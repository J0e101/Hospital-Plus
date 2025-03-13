import json

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth

from HospitalApp.credentials import MpesaAccessToken, LipanaMpesaPpassword
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
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

#M-Pesa API
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "HospitalPlus",
            "TransactionDesc": "Appointment Charges"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        # Parse response
        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        # Save transaction to database
        transaction = Transaction(
            phone_number=phone,
            amount=amount,
            transaction_id=transaction_id,
            status="Success" if result_code == "0" else "Failed"
        )
        transaction.save()

        return HttpResponse(
            f"Transaction ID: {transaction_id}, Status: {'Success' if result_code == '0' else 'Failed'}")


def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})

