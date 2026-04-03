from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    CustomUser, TeamLead, Employee, Project,
    Task, PerformanceRating
)

# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')



# TeamLead Form
class TeamLeadForm(forms.ModelForm):
    class Meta:
        model = TeamLead
        fields = ['name', 'email']

# Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name', 'email', 'team_lead', 'resume_file',
            'skills',  # ✅ Add this
            'age', 'gender', 'education', 'education_field',
            'job_role', 'department',
            'marital_status', 'monthly_income'
        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# Project Form
# ✅ Add required_skills
from django import forms
from .models import Project, TeamLead

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'team_lead', 'domain', 'required_skills', 'deadline', 'criticality']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# Task Assignment Form
# core/forms.py
class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'employee', 'description']

    def __init__(self, *args, **kwargs):
        team_lead = kwargs.pop('team_lead', None)  # get the team lead
        super(TaskAssignForm, self).__init__(*args, **kwargs)

        # Add form-control class
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Filter employee and project by team lead
        if team_lead:
            self.fields['employee'].queryset = Employee.objects.filter(team_lead=team_lead)
            self.fields['project'].queryset = Project.objects.filter(team_lead=team_lead).exclude(domain__isnull=True).exclude(domain__exact='')


# Task Submission Form
class TaskSubmitForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['date_submitted', 'approved']

    def __init__(self, *args, **kwargs):
        super(TaskSubmitForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# Performance Rating Form
class PerformanceRatingForm(forms.ModelForm):
    class Meta:
        model = PerformanceRating
        fields = ['employee', 'rating', 'comments']

    def __init__(self, *args, **kwargs):
        super(PerformanceRatingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# HR Filter Form
class HRFilterForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False)
    team_lead = forms.ModelChoiceField(queryset=TeamLead.objects.all(), required=False)
    task_description = forms.CharField(max_length=255, required=False, label="Task Name")
    submitted = forms.BooleanField(required=False)
    approved = forms.BooleanField(required=False)
    rating_min = forms.IntegerField(required=False, label="Min Rating")

    def __init__(self, *args, **kwargs):
        super(HRFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})
from django import forms
from .models import Employee, TeamLead
from django import forms
from .models import Employee, TeamLead, Project, CustomUser
from django import forms
from .models import Employee, TeamLead

class AllocateEmployeeForm(forms.Form):
    team_lead = forms.ModelChoiceField(queryset=TeamLead.objects.all(), required=True)
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(), 
        widget=forms.CheckboxSelectMultiple
    )

