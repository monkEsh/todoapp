from django.test import TestCase
from django.contrib.auth.models import User
from .models import TodoList
from .forms import UserRegistraionForm


class AddTaskModalTest(TestCase):
    """
    1. Create test user
    2. add task in tasklist
    3. Check task in tasklist
    4. Remove setup

    """
    username = "test-user"
    title1 = "test-title1"
    title2 = "test-title2"

    def setUp(self):
        print("create test user")
        user = User.objects.create(username=self.username,
                                   email="a@a.com",
                                   password="test@123")
        print("create tasklists")
        TodoList.objects.create(title=self.title1,
                                creator=user)
        TodoList.objects.create(title=self.title2,
                                creator=user)

    def test_check_data(self):
        print("retrive data from tasklist")
        title1 = TodoList.objects.get(title=self.title1)
        title2 = TodoList.objects.get(title=self.title2)
        print("check data in tasklist")
        self.assertEqual(title1.title, self.title1)
        self.assertEqual(title2.title, self.title2)


class AddUserFormTest(TestCase):
    """
    1. Create reqiest data
    2. Give that data to form
    3. Check for is valid of not
    """
    def test_valid_form(self):

        data = {"username": "test-user",
                "email": "a@a.com",
                "password": "test123",
                "re_password": "test123"}

        form = UserRegistraionForm(data=data)
        self.assertTrue(form.is_valid())
