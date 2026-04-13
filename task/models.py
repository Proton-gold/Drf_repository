from django.db import models
from accounts.models import User


class Project(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'
        unique_together = ('owner', 'title')


class Status(models.TextChoices):
    TO_DO = 'TO DO'
    IN_PROGRESS = 'IN PROGRESS'
    TEST = 'TEST'
    REJECT = 'REJECT'
    BACKLOG = 'BACKLOG'
    ACCEPTED = 'ACCEPTED'
    FAILED = 'FAILED'


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'task'
