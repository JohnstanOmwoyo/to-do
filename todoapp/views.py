from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from todoapp.models import Task
from todoapp.forms import TaskForm

def home(request):
    return render(request, 'todoapp/home.html')

class TaskCreateView(CreateView):
    model=Task
    form_class=TaskForm
    template_name= 'todoapp/create_task.html'
    success_url=reverse_lazy('task_list')

    def form_valid(self, form):
        '''
        overriding the form_valid() to set the user automatically
        '''
        if self.request.user.is_authenticated:
            form.instance.user=self.request.user  #sets the current user as the task creator
            messages.success(self.request, 'Task created successfully')
        else:
            form.instance.user=None     #allows anonymous user to create a task
        return super().form_valid(form)
    
class TaskListView(ListView):
    model=Task
    template_name='todoapp/task_list.html'
    context_object_name='tasks'

    def get_queryset(self):
        '''filtering tasks by current user'''
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['unassigned_tasks']=Task.objects.filter(user=None)
        return context
        

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model=Task
    form_class=TaskForm
    template_name='todoapp/update_task.html'
    success_url=reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model=Task
    template_name='todoapp/delete_task.html'
    success_url= reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    

# Create your views here.
