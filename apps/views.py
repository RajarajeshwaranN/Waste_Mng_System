from django.shortcuts import render, redirect, get_object_or_404
import mysql.connector as sql
from django.contrib.auth.models import User

from .models import booking
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate
# from django.contrib.auth import get_user_model


# User  = get_user_model()


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
                user = User(username=username, email=email, password=password)
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
        user = authenticate(request, username=email, password=password)

        #user = User.objects.get(email=email)
        print("Email:", email)
        print("Password:", password)

        if user is not None:
            # Successful login
            # Redirect to a dashboard or home page
            login(request, user)
            return redirect('index')  
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
    Booking_data = booking.objects.filter(email=request.user.email)
   # Booking_data = booking.objects.all()

    if request.user.is_authenticated:
        print("User is authenticated:", request.user.email)
        
    else:
        print("User is not authenticated.")

    # if request.user.is_authenticated:
    #     # Filter bookings by the logged-in user's email
    #     Booking_data = booking.objects.filter(email=request.user.email)
    # else:
    #     Booking_data = booking.objects.none()  # Return an empty queryset if the user is not authenticated

    return render(request, 'booking_list.html', {'Booking_data': Booking_data})




def delete_booking(request, email):
    # Ensure the booking exists and belongs to the current user
    Booking = get_object_or_404(booking, email=request.user.email)
    if request.method == "POST":
        Booking.delete()  # Delete the booking
        return redirect('booking_list')  # Redirect to the booking list page
    return render(request, 'delete_confirmation.html', {'Booking': Booking})

#------------Admin dashboard views

from .models import AdminTask
from .forms import AssignTaskForm

def is_admin(user):
    return user.is_staff  # Only staff members are allowed to access the admin dashboard

@user_passes_test(is_admin)
def dashboard(request):
    all_requests = booking.objects.all()
    return render(request, 'admin_dashboard/dashboard.html', {'all_requests': all_requests})

@user_passes_test(is_admin)
def assign_task(request, request_id):
    waste_request = get_object_or_404(booking, id=request_id)
    if request.method == 'POST':
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.request = waste_request
            task.assigned_admin = request.user
            task.save()
            messages.success(request, "Task assigned successfully.")
            return redirect('admin_dashboard:dashboard')
    else:
        form = AssignTaskForm()
    return render(request, 'admin_dashboard/assign_task.html', {'form': form, 'request': waste_request})

@user_passes_test(is_admin)
def update_task_status(request, task_id):
    task = get_object_or_404(AdminTask, id=task_id)
    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
        messages.success(request, "Task status updated successfully.")
        return redirect('admin_dashboard:dashboard')
    return render(request, 'admin_dashboard/update_task.html', {'task': task})