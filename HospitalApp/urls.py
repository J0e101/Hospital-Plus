from django.contrib import admin
from django.urls import path

from HospitalApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index, name='home'),
    path('starter-page/', views.starter, name='starter-page'),
    path('service-details/', views.service, name='service-details'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('departments/', views.deps, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('appointment/', views.appoint, name='appointment'),
    path('contacts/', views.contacts, name='contacts'),
    path('show-appointments/', views.showappoint, name='show-appointments'),
    path('deleteappoint/<int:id>', views.deletappoint),
    path('show-contacts/', views.showcont, name='show-contacts'),
    path('deletecont/<int:id>', views.deletecont),
    path('editappoint/<int:id>', views.editappoint, name= 'edit-appointment-details'),
    path('editcont/<int:id>', views.editcont, name= 'edit-contact-details'),
    path('', views.register, name= 'register'),
    path('login/', views.login_view, name= 'login'),

    #M-Pesa API
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('transactions/', views.transactions_list, name='transactions'),
]
