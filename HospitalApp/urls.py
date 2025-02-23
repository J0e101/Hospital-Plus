from django.contrib import admin
from django.urls import path
from HospitalApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('starter-page/', views.starter, name='starter-page'),
    path('service-details', views.service, name='service-details'),

]
