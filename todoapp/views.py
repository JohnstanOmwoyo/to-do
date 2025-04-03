from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from todoapp.models import Task
from todoapp.forms import TaskForm

def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()    #saves the user

            #Autologin the user after registration
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'failed to create account')
    else:
        form=UserCreationForm()
    return render(request, 'todoapp/register.html', {'form':form})

@login_required
def profile_view(request):
    return render(request, 'todoapp/profile.html')

def home(request):
    return render(request, 'todoapp/home.html')

class UserLoginView(LoginView):
    '''
    View to handle user login
    '''
    template_name = 'todoapp/login.html'
    success_url = reverse_lazy('profile')
    redirect_authenticated_user = True

    def form_valid(self, form):
        '''
        override form_valid to add a success message
        '''
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        '''
        override form_invalid to add an error message
        '''
        messages.error(self.request, 'Invalid credentials')
        return super().form_invalid(form)
    
    def get(self, request):
        return render(request, 'todoapp/login.html')
    
    def post(self, request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('todoapp:task_list')
        return render(request, 'todoapp/login.html', {'error': 'Invalid credentials'})

class UserLogoutView(LogoutView):
    '''
    Generic class-based view for logging out a user.
    This view logs out the user and redirects them to the login page.
    '''
    template_name = 'todoapp/logout.html'
    next_page = reverse_lazy('login')


class TaskCreateView(LoginRequiredMixin, CreateView):
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