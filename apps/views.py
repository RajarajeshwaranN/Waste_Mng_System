from django.shortcuts import render, redirect
import mysql.connector as sql
from .models import user,booking
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login_view(request):
    return render(request, 'login.html')

def signup(request):
    
    if request.method=="POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password == confirm_password:
            # Save the data to the database
                User = user(username=username, email=email, password=password, confirm_password=confirm_password)
                User.save()
                messages.success(request, 'Signup successful!')
                return redirect('login')  # Redirect to login page after signup
            else:
                messages.error(request, 'Passwords do not match.')

    return render(request,'login.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists in the database
        
        try:
            User = user.objects.get(email=email)
            print("Email:", email)
            print("Password:", password)

            if User.password == password:
                # Successful login
                # Redirect to a dashboard or home page
                return redirect('index')  # Replace 'home' with the name of your target URL
            else:
                messages.error(request, 'Invalid password')
        except user.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'login.html')

def booking_view(request):
    if request.method == 'POST':
        # Get form data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        date = request.POST.get('date')
        time = request.POST.get('time')
        address = request.POST.get('address')
        
         # Check for empty fields
        if not all([name, email, mobile, date, time, address]):
            return HttpResponse("Please fill out all fields.")
        
        # Process the form data (e.g., save to the database or perform other actions)
        # Here, you could add logic to save data to your database
        book = booking.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            date=date,
            time=time,
            address=address
        )
        book.save()

        return HttpResponse("Booking submitted successfully!")

    # Render the form
    return render(request, 'booking.html')