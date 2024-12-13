from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Workers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=255, null=True)
    course_completed = models.CharField(max_length=255, null=True)
    certificate = models.FileField(upload_to='certificates/', null=True)
    image = models.ImageField(upload_to='images/', null=True)  
    status = models.CharField(max_length=20, default='Pending')
    
class Project(models.Model):
    client_name = models.CharField(max_length=255, null=True)
    client_email = models.EmailField(null=True)
    client_phone = models.CharField(max_length=15, null=True)
    client_address = models.TextField(null=True)
    worker = models.ForeignKey('Workers', on_delete=models.CASCADE, null=True)
    project_name = models.CharField(max_length=255, null=True)
    project_status = models.CharField(max_length=20, default='Pending')
    description = models.TextField(null=True)
    requirements = models.TextField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    attachment = models.FileField(upload_to='project_attachments/', null=True)

class Team(models.Model):
    team_leader = models.ForeignKey(Workers, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
class Python(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=20, default='Developer')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

class Work(models.Model):
    developer = models.ForeignKey(Python, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    team_leader = models.ForeignKey(Workers, on_delete=models.CASCADE)
    module = models.TextField(null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    upload = models.FileField(upload_to='work_submissions/', null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    submit_date = models.DateField(null=True, blank=True)

class DailyReport(models.Model):
    developer = models.ForeignKey(Python, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    team_leader = models.ForeignKey(Workers, on_delete=models.CASCADE,null=True)
    report_status = models.CharField(max_length=20, default='Pending',null=True)
    report_date = models.DateField(default=timezone.now,null=True)
    description = models.TextField(null=True)
    work_report = models.FileField(upload_to='daily_reports/', null=True, blank=True)
    class Meta:
        unique_together = ('developer', 'project', 'report_date')

class DailyReportTeamLeader(models.Model):
    team_leader = models.ForeignKey(Workers, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    report_status = models.CharField(max_length=20, default='Pending')
    report_date = models.DateField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
    work_report = models.FileField(upload_to='daily_reports/', null=True, blank=True)

class Notification(models.Model):
    team_leader = models.ForeignKey(Workers, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255,null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class DeveloperAssignment(models.Model):
    developer = models.ForeignKey(Python, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_date = models.DateField(default=timezone.now)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Assigned', 'Assigned'), ('Completed', 'Completed')])

