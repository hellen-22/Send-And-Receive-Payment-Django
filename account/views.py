from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as user_login, authenticate
from django.views.generic import CreateView

from .models import *
from .forms import *

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

                return redirect('login')
        else:
            messages.info('Passwords do not match')

    else:
        return render(request, 'user/register.html')

def login(request):
    form = LogInForm(request.POST or None)

    msg = None

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                user_login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid Credentials, Try Again")
        else:
            messages.error(request, "Error Valid Details, Try Again")

    return render(request, "user/login.html", {"form": form, "msg": msg})


def home(request):
    return render(request, 'account/home.html')

class CreateTransactionView(CreateView):
    model = Transactions
    fields = ['receiver', 'amount', 'payment_method']
    template_name = 'transactions/add_transaction.html'