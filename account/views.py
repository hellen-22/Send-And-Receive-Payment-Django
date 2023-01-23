from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.views.generic import CreateView

from .models import *

# Create your views here.
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')

            elif User.objects.filter(phone_number=phone_number).exists():
                messages.info(request, 'Phone Number already exists')

            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, phone_number=phone_number, password=password)
                user.save()

                return redirect('home')
        else:
            messages.info('Passwords do not match')

    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)

        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

class CreateTransactionView(CreateView):
    model = Transactions
    fields = ['receiver_id', 'amount', 'payment_method']
    template_name = 'add_transaction.html'