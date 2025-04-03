from django.urls import path
from todoapp.views import TaskCreateView, TaskListView, TaskUpdateView, TaskDeleteView
from todoapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("create_task/", TaskCreateView.as_view(), name="create_task"),
    path("task_list/", TaskListView.as_view(), name="task_list"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="update_task"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete_task"),
    # path('login/', LoginView.as_view(template_name='todoapp/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login', template_name='todoapp/logout.html'), name='logout'),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="todoapp/login.html"), name="login"),
    path('accounts/profile/', views.profile_view, name='profile'),
    
]