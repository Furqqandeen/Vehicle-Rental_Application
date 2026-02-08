from django.urls import path
from .import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views





app_name='vehicles'

urlpatterns = [
    
    path('', views.home, name='home'),
    path('vehicle/<str:vehicle_type>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vehicle/<int:vehicle_id>/rules/', views.rules, name='rules'),
    path('about/',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('rules_reg/',views.rules_regulation,name='rules_reg'),
    path('vehicle/<int:vehicle_id>/rental/', views.rental_form, name='rental'),
    path('success/',views.success_page,name='success'),
    path('my_rentals/',views.my_rentals,name='my_rentals'),
    path('vehicle_detail/<int:vehicle_id>/',views.vehicle_detail,name='vehiclez'),
    path('rentals/<int:rental_id>/cancel/', views.cancel_rental, name='cancel_rental'),
    
   
    
]
