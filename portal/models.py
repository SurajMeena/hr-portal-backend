from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices


class PositionChoices(TextChoices):
    MANAGER = 'Manager', 'Manager'
    DEVELOPER = 'Developer', 'Developer'
    DESIGNER = 'Designer', 'Designer'
    ANALYST = 'Analyst', 'Analyst'
    INTERN = 'Intern', 'Intern'
    HR = 'HR', 'HR'


class Employee(AbstractUser):
    name = models.CharField(max_length=50, default=None)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50, choices=PositionChoices.choices, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_updated = models.DateField(auto_now=True)
    start_date = models.DateField(default=None)
    company = models.CharField(max_length=50, default="Searcee")

    def __str__(self):
        return self.username


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    task_type = models.CharField(max_length=50, choices=[('file_upload', 'File Upload'), ('text_input', 'Text Input')])

    def __str__(self):
        return self.title


class NewHireTask(models.Model):
    id = models.AutoField(primary_key=True)
    new_hire_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateField()
    file_upload = models.FileField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.new_hire_id
