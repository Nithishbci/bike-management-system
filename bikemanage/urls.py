"""
URL configuration for bikemanage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from service import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.enroll_new_rider, name='enroll_new_rider'),
    path('login/', views.welcome_rider, name='user_login'),
    path('dashboard/', views.my_dashboard, name='my_dashboard'),
    path('logout/', views.rider_logout, name='rider_logout'),
    path('book-service/', views.arrange_bike_service, name='arrange_bike_service'),
    path('my-bookings/', views.my_booking_list, name='my_booking_list'),
    path('edit-booking/<int:booking_id>/', views.edit_my_booking, name='edit_my_booking'),
    path('cancel-booking/<int:booking_id>/', views.cancel_my_booking, name='cancel_my_booking'),
    path('manage/bookings/unassigned/', views.list_unassigned_bookings, name='list_unassigned_bookings'),
    path('manage/bookings/assign/<int:booking_id>/', views.assign_mechanic, name='assign_mechanic'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/bookings/all/', views.see_all_bookings, name='see_all_bookings'),
    path('manage/bookings/status/<int:booking_id>/', views.update_service_status, name='update_service_status'),
    path('invoice/<int:booking_id>/', views.view_invoice, name='view_invoice'),






]
