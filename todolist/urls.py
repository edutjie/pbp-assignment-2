from django.urls import path
from todolist.views import create_task, show_todolist, register, login_user, logout_user

app_name = "todolist"
urlpatterns = [
    path("", show_todolist, name="show_todolist"),
    path("login/", login_user, name="login"),
    path("register/", register, name="register"),
    path("create-task/", create_task, name="create_task"),
    path("logout/", logout_user, name="logout"),
]
