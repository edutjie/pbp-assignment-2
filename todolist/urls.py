from django.urls import path
from todolist.views import (
    add_task,
    create_task,
    delete_task,
    show_todolist,
    register,
    login_user,
    logout_user,
    update_finished,
    show_json,
)

app_name = "todolist"
urlpatterns = [
    path("", show_todolist, name="show_todolist"),
    path("login/", login_user, name="login"),
    path("register/", register, name="register"),
    path("create-task/", create_task, name="create_task"),
    path("logout/", logout_user, name="logout"),
    path("delete-task/<int:id>", delete_task, name="delete_task"),
    path("update-finished/<int:id>", update_finished, name="update_finished"),
    path("json/", show_json, name="show_json"),
    path("add/", add_task, name="add_task"),
]
