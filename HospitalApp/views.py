from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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

def editappoint(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == "POST":
        appointment.name = request.POST.get('name')
        appointment.email = request.POST.get('email')
        appointment.phone_number = request.POST.get('phone_number')
        appointment.date_of_birth = request.POST.get('date_of_birth')
        appointment.department = request.POST.get('department')
        appointment.doctor = request.POST.get('doctor')
        appointment.message = request.POST.get('message')

        appointment.save()
        return redirect('/show-appointments')

    else:
        return render(request, 'editappointment.html', {'appointment': appointment})

def editcont(request, id):
    contact = get_object_or_404(Contact, id=id)
    if request.method == "POST":
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.subject = request.POST.get('subject')
        contact.message = request.POST.get('message')

        contact.save()
        return redirect('/show-contacts')

    else:
        return render(request, 'editcontacts.html', {'contact': contact})

def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')
