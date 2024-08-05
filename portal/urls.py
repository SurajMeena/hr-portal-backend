from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-hires", views.fetch_new_hires, name="fetch_new_hires"),
    path("new-hires/create", views.create_new_hire, name="create_new_hire"),
    path("new-hires/<int:user_id>", views.fetch_employee_info, name="get_employee_info"),
    path("new-hires/<int:user_id>/tasks", views.fetch_user_tasks, name="fetch_user_tasks"),
    path("tasks", views.fetch_tasks, name="fetch_tasks"),
    path("tasks/create", views.create_task, name="create_task"),
    path("tasks/assign", views.assign_task, name="assign_task"),
    path("new-hires/<int:task_id>/update", views.update_task, name="update_task"),
]
