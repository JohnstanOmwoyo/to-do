from django.contrib import admin
from todoapp.models import Task, Reminder, Category

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Reminder)



# Register your models here.
