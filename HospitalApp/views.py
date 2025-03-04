from django.shortcuts import render, redirect
from HospitalApp.models import *

# Create your views here.
def service(request):
    return render(request, 'service-details.html')

def starter(request):
    return render(request, 'starter-page.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def doctors(request):
    return render(request, 'doctors.html')

def deps(request):
    return render(request, 'departments.html')

def contacts(request):
    if request.method == "POST":
        mycontacts = Contact(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )

        mycontacts.save()
        return redirect('/contacts')
    else:
        return render(request, 'contacts.html')

def appoint(request):
    if request.method == "POST":
        myappointments = Appointment(
            name = request.POST['name'],
            email = request.POST['email'],
            phone_number = request.POST['phone_number'],
            date_of_birth = request.POST['date_of_birth'],
            department = request.POST['department'],
            doctor = request.POST['doctor'],
            message = request.POST['message']
        )
        myappointments.save()
        return redirect('/show-appointments')

    else:
        return render(request, 'appointment.html')

def showappoint(request):
    all = Appointment.objects.all()
    return render(request, 'showappointments.html', {'appointments': all})

def deletappoint(request, id):
   deleteappointment= Appointment.objects.get(id=id)
   deleteappointment.delete()
   return redirect('/show-appointments')

def showcont(request):
    all = Contact.objects.all()
    return render(request, 'showcontacts.html', {'contacts': all})

def deletecont(request, id):
    deletecontact= Contact.objects.get(id=id)
    deletecontact.delete()
    return redirect('/show-contacts')


