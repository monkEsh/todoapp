from django.conf.urls import url, include
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'user', views.UserViewSet)
#router.register(r'todolist', views.TodoListViewSet)
#router.register(r'todo', views.TodoViewSet)

urlpatterns = [
    url(r'^login/', views.login_view, name="login"),
    url(r'^register/', views.register_view, name="register"),
    url(r'^logout/', views.login_view, name="logout"),
    url(r'^index/', views.index, name="index"),
    url(r'^todo-list/', views.TodoViewSet.as_view(), name="todo-list"),
    url(r'^todo/', views.TodoListView.as_view(), name="todo"),
    url(r'^todo-tasks/(?P<tasklist>\w+)', views.todo_tasks, name="tasks"),
    url(r'^change-status/', views.update_status, name="update-task"),
    url(r'^add-task/', views.add_task, name="add-task"),
    url(r'add_task_list/', views.add_task_list, name="add_task_list"),
    url(r'edit-task/', views.edit_task_page, name="edit_task"),
    url(r'edit-task-data/', views.edit_task, name="edit")
]
