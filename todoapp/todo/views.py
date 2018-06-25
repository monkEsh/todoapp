from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout)
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)
from rest_framework.mixins import (
    CreateModelMixin
)
from rest_framework.response import Response
from .models import TodoList, Todo
from .serializers import (
    UserSerializer,
    TodoListSerializer,
    TodoSerializer
)
from .forms import (
    UserLoginForm,
    UserRegistraionForm,
)
from django.shortcuts import render, redirect
from .permissions import IsCreatorOrReadOnly
import json
# Create your views here.

UserModel = get_user_model()


"""
User auth and session
"""
def login_view(request):
    data = {"title": "Login"}
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        login(request, user)
        print(request.user)
        if request.user.is_authenticated:
            user_obj = UserModel.objects.filter(username=username).filter(is_staff=True)
            print("Data is ", type(user_obj.count()))
            if user_obj.count() == 1:
                request.session["admin"] = True

            return redirect('index')

    data["form"] = form
    return render(request, "pages/form.html", data)


def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    data = {"title": "Sign Up"}
    form = UserRegistraionForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        new_user.set_password(password)
        new_user.save()
        return redirect('index')

    data["form"] = form
    return render(request, "pages/form.html", data)


"""
End User auth and session
"""

"""
User interface with system
"""


def index(request):
    try:
        if request.user.is_authenticated:
            return render(request, "pages/index.html")
        else:
            return redirect('login')

    except:
        return redirect('login')


def todo_tasks(request, tasklist):
    data = {"total_tasks": {},
            "done_tasks": {},
            "inprogress": {},
            "open_tasks": {},
            "tasklist": tasklist}
    qs = TodoList.objects.get(title=tasklist)

    qs = Todo.objects.filter(todolist=qs)
    data["total_tasks"] = qs.count()
    data["open_tasks"]["count"] = qs.filter(status="Open").count()
    data["done_tasks"]["count"] = qs.filter(status="Done").count()
    data["inprogress"]["count"] = qs.filter(status="In-Progress").count()

    data["open_tasks"] = qs.filter(status="Open")
    data["done_tasks"] = qs.filter(status="Done")
    data["inprogress"] = qs.filter(status="In-Progress")
    # return JsonResponse(data)
    return render(request, "pages/task-details.html", data)


def update_status(request):
    tasklist = request.GET.get("tasklist")
    pk = request.GET.get("pk")
    status = request.GET.get("status")
    qs = Todo.objects.get(pk=pk)
    qs.status = status
    if status == "Done":
        qs.close()
    if status == "Open":
        qs.reopen()
    qs.save()

    return redirect("tasks", tasklist=tasklist)


@csrf_exempt
def add_task(request):
    data = {"success": False}
    try:
        title = request.POST.get("title")
        status = request.POST.get("status")
        desc = request.POST.get("desc")
        tasklist = request.POST.get("tasklist")

        todolist_obj = TodoList.objects.get(title=tasklist)
        user = request.user
        todo = Todo.objects.filter(title=title).count()
        if todo == 0:
            todo_obj = Todo.objects.create(creator=user,
                                           todolist=todolist_obj,
                                           description=desc,
                                           status=status,
                                           title=title)
            todo_obj.save()
            data["message"] = "Data Saved"
            data["success"] = True
        else:
            raise Exception("Task with same title already exists")
    except Exception as ex:
        data["message"] = "Failed to save data [%s]" % ex
    finally:
        return JsonResponse(data)


@csrf_exempt
def add_task_list(request):
    data = {"success": False}
    try:
        title = request.POST.get("title")
        user = request.user
        todolist = TodoList.objects.filter(title=title).count()
        if todolist == 0:
            todolist_obj = TodoList.objects.create(title=title,
                                                   creator=user)
            todolist_obj.save()
            data["success"] = True
            data["message"] = "Data Saved"
        else:
            raise Exception("List with same name exist")
    except Exception as ex:
        data["message"] = "Failed to save data [%s]" % ex
    finally:
        return JsonResponse(data)

"""
User interface with system
"""

"""
Restful API
"""


class TodoListView(CreateModelMixin, ListAPIView):
    """
    API endpoint to CRUD on todolist
    """
    lookup_field = "title"
    serializer_class = TodoListSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_queryset(self):
        qs = TodoList.objects.all()
        try:
            query = self.request.GET.get("q")
            qs = qs.filter(
                Q(title__icontains=query)
            ).distinct()
        except Exception as ex:
            pass
        return qs

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as ex:
            return Response("Failed to save data [%s]" % ex)


class TodoViewSet(CreateModelMixin, ListAPIView):
    """
    API endpoint to CRUD new subtask
    """
    lookup_field = "description"

    serializer_class = TodoSerializer
    permission_classes = [IsCreatorOrReadOnly]
    # queryset = Todo.objects.all()

    def get_queryset(self):
        qs = Todo.objects.all()
        try:
            query = self.request.GET("q")
            if query is not None:
                qs = qs.filter(
                    Q(description__iscontains=query) |
                    Q(is_finished__iscontains=query)
                ).distinct()
        except:
            pass

        return qs

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as ex:
            return Response("Failed to save data [%s]" % ex)
