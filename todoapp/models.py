from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORY_CHOICES=[
        ('WORK', 'Work'),
        ('PERSONAL', 'Personal'),
        ('PERSONAL', 'Personal'),
    ]

    name=models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES=[
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]


    title=models.CharField(max_length=25, blank=False)
    description=models.TextField()
    completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    due_date=models.DateField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority=models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='M')


    def __str__(self):
        return f'complete the Task:{self.title} by {self.due_date}'
    

class Reminder(models.Model):
    task=models.OneToOneField(Task, on_delete=models.CASCADE)
    reminder_time=models.DateTimeField()

    def __str__(self):
        return f'Reminder for{self.task.title} at {self.reminder_time}'



# Create your models here.
