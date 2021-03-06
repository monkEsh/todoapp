from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from .models import TodoList, Todo, TodoAction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class TodoActionsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = TodoAction
        fields = "__all__"


class TodoSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    task = TodoActionsSerializer(read_only=True, many=True)

    class Meta:
        model = Todo
        fields = [
            "title",
            "description",
            "created_at",
            "creator",
            "status",
            "task"
        ]


class TodoListSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = TodoList
        fields = [
            "title",
            "created",
            "creator",
            "todos"
        ]

    def validate_title(self, value):
        qs = TodoList.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.count() >= 1:
            raise serializers.ValidationError("Task with same name already exist")
        return value



