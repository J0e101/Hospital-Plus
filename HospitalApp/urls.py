from django.contrib import admin
from django.urls import path
from HospitalApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('starter-page/', views.starter, name='starter-page'),
    path('service-details/', views.service, name='service-details'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('departments/', views.deps, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('appointment/', views.appoint, name='appointment'),
    path('contacts/', views.contacts, name='contacts'),
    path('show-appointments/', views.showappoint, name='show-appointments'),
    path('deleteapp/<int:id>', views.deletappoint),
    path('show-contacts/', views.showcont, name='show-contacts'),
    path('deletecont/<int:id>', views.deletecont),


]
