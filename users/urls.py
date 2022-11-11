from django.urls import path
from .views import index, create_faculty, create_department, register_lecturer, register_student, user_login, user_logout, dashboard


urlpatterns = [
    path('', index, name='home'),
    path('super_admin/create/faculty', create_faculty, name='create_faculty'),
    path('super_admin/create/department', create_department, name='create_department'),
    path('users/register/lecturer', register_lecturer, name='register_lecturer'),
    path('users/register/student', register_student, name='register_student'),
    path('users/login', user_login, name='login'),
    path('users/logout', user_logout, name='logout'),
    path('dashboard', dashboard, name='dashboard')
]
