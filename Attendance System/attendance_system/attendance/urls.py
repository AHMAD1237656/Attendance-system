# attendance/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views   # ✅ ye import zaroori hai
from . import views

urlpatterns = [
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.mark_attendance, name='mark_attendance'),
    path('attendance/update/<int:id>/', views.update_attendance, name='update_attendance'),
    path('attendance/delete/<int:id>/', views.delete_attendance, name='delete_attendance'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('monthly_report/', views.monthly_report, name='monthly_report'),
    path('dashboard/', views.dashboard, name='dashboard'),  # ✅ dashboard URL
]
