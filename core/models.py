# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("HR", "HR"),
        ("TL", "Team Lead"),
        ("EMP", "Employee"),
        ("Manager", "Manager"),
        ("Guest", "Guest"),  
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Guest")
    def __str__(self):
        return self.username
class TeamLead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    team_lead = models.ForeignKey(TeamLead, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(
    CustomUser, 
    on_delete=models.CASCADE, 
    limit_choices_to={'role': 'Manager'}, 
    null=True, 
    blank=True
)

    domain = models.CharField(max_length=100, null=True, blank=True)
    required_skills = models.TextField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    criticality = models.IntegerField(default=3)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team_lead = models.ForeignKey(TeamLead, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(null=True, blank=True)  # e.g., "Python, Django, HTML"
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    education = models.IntegerField(null=True, blank=True)
    education_field = models.CharField(max_length=100, null=True, blank=True)
    job_role = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=[
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced')
    ], null=True, blank=True)
    monthly_income = models.FloatField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  
class PerformanceRating(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField(blank=True)
    date_rated = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.employee.user.username} - {self.rating}"
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    team_lead = models.ForeignKey(TeamLead, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date_assigned = models.DateField(auto_now_add=True)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    date_submitted = models.DateField(null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.approved and self.date_submitted is None:
            from django.utils import timezone
            self.date_submitted = timezone.now().date()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.project.name} - {self.employee.name}"
class TrainingCourse(models.Model):
    skill = models.CharField(max_length=100)
    course_name = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    def __str__(self):
        return f"{self.skill} - {self.course_name}"
class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    resume_file = models.FileField(upload_to="resumes/")
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )
    prediction = models.CharField(max_length=20, blank=True, null=True)
    notified = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} - {self.status}"


