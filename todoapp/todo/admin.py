from django.contrib import admin
from .models import Todo, TodoList
# Register your models here.


admin.site.register(Todo)
admin.site.register(TodoList)
