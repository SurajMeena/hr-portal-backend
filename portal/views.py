import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.http import HttpResponse, FileResponse
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Employee, NewHireTask, Task


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def fetch_employee_info(request, user_id):
    try:
        employee = Employee.objects.get(id=user_id)
        total_tasks = NewHireTask.objects.filter(new_hire_id=employee).count()
        completed_tasks = NewHireTask.objects.filter(
            new_hire_id=employee, is_completed=True
        ).count()
        return JsonResponse(
            {
                "id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "phone": employee.phone,
                "address": employee.address,
                "department": employee.department,
                "position": employee.position,
                "salary": employee.salary,
                "start_date": employee.start_date.strftime("%Y-%m-%d"),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "company": employee.company,
            }
        )
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)


def fetch_new_hires(request):
    start_date = datetime.now() + timedelta(days=30)
    employees = Employee.objects.filter(start_date__lt=start_date).exclude(
        position="HR"
    )
    employee_data = []
    for employee in employees:
        total_tasks = NewHireTask.objects.filter(new_hire_id=employee).count()
        completed_tasks = NewHireTask.objects.filter(
            new_hire_id=employee, is_completed=True
        ).count()
        employee_data.append(
            {
                "id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "start_date": employee.start_date.strftime("%Y-%m-%d"),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "phone": employee.phone,
            }
        )
    return JsonResponse(employee_data, safe=False)


@require_http_methods(["POST"])
def create_new_hire(request):
    try:
        data = json.loads(request.body)
        employee = Employee(
            name=data["name"],
            email=data["email"],
            phone=data["contactNo"],
            address=data.get("address", None),
            department=data.get("department", None),
            position=data.get("position", None),
            salary=data.get("salary", None),
            start_date=parse_date(data["dateOfJoining"]),
            username=data["name"].lower().replace(" ", "_"),
            password=data.get("password", generate_password()),
        )
        employee.full_clean()  # Validate the model fields
        employee.save()
        return JsonResponse(
            {"message": "New hire created successfully", "id": employee.id}, status=201
        )
    except (KeyError, ValidationError) as e:
        return JsonResponse({"error": str(e)}, status=400)


# def fetch_task_files(request, task_id):
#     try:
#         new_hire_task = NewHireTask.objects.get(id=task_id)
#         if new_hire_task.file_upload:
#             return FileResponse(new_hire_task.file_upload, as_attachment=True)
#     except NewHireTask.DoesNotExist:
#         return JsonResponse({"error": "Task not found"}, status=404)


@require_http_methods(["GET"])
def fetch_user_tasks(request, user_id):
    try:
        employee = Employee.objects.get(id=user_id)
        tasks = NewHireTask.objects.filter(new_hire_id=employee)
        task_data = []
        for task in tasks:
            task_data.append(
                {
                    "task_id": task.task_id.id,
                    "title": task.task_id.title,
                    "description": task.task_id.description,
                    "is_completed": task.is_completed,
                    "completion_date": (
                        task.completion_date.strftime("%Y-%m-%d")
                        if task.completion_date
                        else None
                    ),
                    "type": task.task_id.task_type,
                    "file_upload": task.file_upload.url if task.file_upload else None,
                    "response": task.response,
                    "comment": task.comment,
                }
            )
        return JsonResponse(task_data, safe=False)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)


@require_http_methods(["GET"])
def fetch_tasks(request):
    tasks = Task.objects.all()
    task_data = []
    for task in tasks:
        task_data.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "task_type": task.task_type,
            }
        )
    return JsonResponse(task_data, safe=False)


@require_http_methods(["POST"])
def create_task(request):
    try:
        data = json.loads(request.body)
        if Task.objects.filter(title=data["title"]).exists():
            return JsonResponse(
                {"error": "Task with this title already exists"}, status=400
            )
        task = Task(
            title=data["title"], description=data["description"], task_type=data["type"]
        )
        task.full_clean()  # Validate the model fields
        task.save()
        return JsonResponse(
            {"message": "Task created successfully", "id": task.id}, status=201
        )
    except (KeyError, ValidationError) as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_http_methods(["POST"])
def assign_task(request):
    try:
        data = json.loads(request.body)
        employee = Employee.objects.get(id=data["new_hire_id"])
        task = Task.objects.get(id=data["task_id"])
        if NewHireTask.objects.filter(new_hire_id=employee, task_id=task).exists():
            return JsonResponse(
                {"error": "Task already assigned to this employee"}, status=400
            )
        new_hire_task = NewHireTask(
            new_hire_id=employee,
            task_id=task,
            is_completed=False,
            completion_date=parse_date(data["completion_date"]),
            file_upload=data.get("file_upload", None),
            comment=data.get("comment", ""),
        )
        new_hire_task.full_clean()  # Validate the model fields
        new_hire_task.save()
        return JsonResponse(
            {"message": "Task assigned successfully", "id": new_hire_task.id},
            status=201,
        )
    except (KeyError, Employee.DoesNotExist, Task.DoesNotExist, ValidationError) as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_http_methods(["POST"])
@csrf_exempt
def update_task(request, task_id):
    try:
        data = json.loads(request.POST["json"])
        new_hire_task = NewHireTask.objects.get(id=task_id)
        new_hire_task.is_completed = False if data["status"] == "pending" else True
        new_hire_task.completion_date = parse_date(data["completionDate"])
        if "files" in request.FILES:
            for file in request.FILES.getlist("files"):
                new_hire_task.file_upload = file
                new_hire_task.save()
        new_hire_task.comment = data["comment"]
        new_hire_task.full_clean()  # Validate the model fields
        new_hire_task.save()
        return JsonResponse({"message": "Task updated successfully"}, status=200)
    except (KeyError, NewHireTask.DoesNotExist, ValidationError) as e:
        return JsonResponse({"error": str(e)}, status=400)


def generate_password():
    import random
    import string

    return "".join(random.choices(string.ascii_letters + string.digits, k=8))
