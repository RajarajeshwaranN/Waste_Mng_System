from django.shortcuts import render, redirect, get_object_or_404
import mysql.connector as sql
from .models import User,booking
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



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
                user = User(username=username, email=email, password=password, confirm_password=confirm_password)
                user.save()
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
        

        user = User.objects.get(email=email)
        print("Email:", email)
        print("Password:", password)

        if user.password == password:
            # Successful login
            # Redirect to a dashboard or home page
            return redirect('index')  # Replace 'home' with the name of your target URL
        else:
            messages.error(request, 'Invalid password')
       

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
        waste_type = request.POST.get('waste')
        quantity = request.POST.get('quantity')
        
         # Check for empty fields
        if not all([name, email, mobile, date, time, address,waste_type,quantity]):
            return HttpResponse("Please fill out all fields.")
        
        # Process the form data (e.g., save to the database or perform other actions)
        # Here, you could add logic to save data to your database
        book = booking.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            date=date,
            time=time,
            address=address,
            waste_type = waste_type,
            quantity = quantity
        )
        book.save()

        return redirect('booking_list')

    # Render the form
    return render(request, 'booking.html')

#logout function---------
def logout_view(request):
    logout(request)
    return redirect('login') 




def booking_list(request):
    # if request.user.is_authenticated:
    #     print("User is authenticated:", request.user.email)
    # else:
    #     print("User is not authenticated.")

    if request.user.is_authenticated:
        # Filter bookings by the logged-in user's email
        Booking_data = booking.objects.filter(email=request.user.email)
    else:
        Booking_data = booking.objects.none()  # Return an empty queryset if the user is not authenticated

    return render(request, 'booking_list.html', {'Booking_data': Booking_data})




def delete_booking(request, email):
    # Ensure the booking exists and belongs to the current user
    Booking = get_object_or_404(booking, email=request.user.email)
    if request.method == "POST":
        Booking.delete()  # Delete the booking
        return redirect('booking_list')  # Redirect to the booking list page
    return render(request, 'delete_confirmation.html', {'Booking': Booking})
