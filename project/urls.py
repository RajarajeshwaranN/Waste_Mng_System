"""
URL configuration for wastesys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apps/', include('apps.urls')),
    path('',include('apps.urls')),
    path('apps/signup/', views.signup, name='signup'),
    path('apps/login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('booking/', views.booking_view, name='booking'),
    path('logout/', views.logout_view, name='logout'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/delete/<int:id>/', views.delete_booking, name='delete_booking'),
    path('update-booking/', views.update_booking, name='update_booking'),

    
    path('admin', views.dashboard, name='dashboard'),
    path('assign/<int:request_id>/', views.assign_task, name='assign_task'),
    path('update-status/<int:task_id>/', views.update_task_status, name='update_task_status'),

    path('users/', views.users_list, name='users_list'),
    path('users/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),


]
