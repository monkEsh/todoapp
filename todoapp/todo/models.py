from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class TodoList(models.Model):
    title = models.CharField(max_length=200, default='Untitled', unique=True)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User,
                                related_name="todolist",
                                on_delete=models.CASCADE)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.title


class Todo(models.Model):
    status = (
        ("Undone", "Undone"),
        ("In-Progress", "In-Progress"),
        ("Done", "Done")

    )
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)
    is_finished = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=status, default="Done")
    creator = models.ForeignKey(User,
                                related_name='user',
                                on_delete=models.CASCADE)
    todolist = models.ForeignKey(TodoList,
                                 related_name='todos',
                                 on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title

    def close(self):
        self.status = "Done"
        self.finished_at = timezone.now()
        TodoAction.objects.create(action_taken="Updated Status to done",
                                  user=self.creator,
                                  task_name=self)
        self.save()

    def reopen(self):
        self.status = "Undone"
        self.finished_at = None
        TodoAction.objects.create(action_taken="Updated Status to undone",
                                  user=self.creator,
                                  task_name=self)
        self.save()

    def in_progress(self):
        TodoAction.objects.create(action_taken="Updated Status to In-Progress",
                                  user=self.creator,
                                  task_name=self)

    def update_title(self, title, user):
        status = False
        try:
            self.title = title
            TodoAction.objects.create(action_taken="Updated title",
                                      user=user,
                                      task_name=self)
            self.save()
            status = True
        except Exception as ex:
            pass
        return status

    def update_description(self, description, user):
        status = False
        try:
            self.description = description
            TodoAction.objects.create(action_taken="Updated description",
                                      user=user,
                                      task_name=self)
            self.save()
            status = True
        except Exception as ex:
            pass
        return status

    def update_status(self, status, user):
        result = False
        try:
            self.status = status
            TodoAction.objects.create(action_taken="Updated status",
                                      user=user,
                                      task_name=self)
            self.save()
            result = True
        except Exception as ex:
            pass
        return result


class TodoAction(models.Model):
    action_taken = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,
                             related_name="actor",
                             on_delete=models.CASCADE)
    task_name = models.ForeignKey(Todo,
                                  related_name="task",
                                  on_delete=models.CASCADE)

    class Meta:
        ordering = ('time',)

    def __str__(self):
        return self.action_taken


