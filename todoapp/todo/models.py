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
        ("Open", "Open"),
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
        return self.description

    def close(self):
        self.status = "Done"
        self.finished_at = timezone.now()
        self.save()

    def reopen(self):
        self.status = "Open"
        self.finished_at = None
        self.save()

