from django.shortcuts import render, redirect, get_object_or_404
import mysql.connector as sql
from django.contrib.auth.models import User

from .models import booking, AdminTask
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from .models import AdminTask
from .forms import AssignTaskForm


# Create your views here.


def index(request):
    return render(request, 'index.html')


# def login_view(request):
#     return render(request, 'login.html')

def signup(request):
    
    if request.method=="POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password == confirm_password:
            # Save the data to the database
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                    return redirect('login')
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Signup successful!')
                return redirect('login')  # Redirect to login page after signup
            else:
                messages.error(request, 'Passwords do not match.')

    return render(request,'login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists in the database
        user = authenticate(request, username=username, password=password)

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



#-------Booking List of the user------
def booking_list(request):
    Booking_data = booking.objects.filter(email=request.user.email)
   # Booking_data = booking.objects.all()

    for booking_item in Booking_data:
        task = AdminTask.objects.filter(request=booking_item).first()  # Get the latest assigned task (or whatever logic you want)

        booking_item.status = task.status if task else "pending"


    return render(request, 'booking_list.html', {'Booking_data': Booking_data})




def delete_booking(request, id):
    # Ensure the booking exists and belongs to the current user
    Booking = get_object_or_404(booking, pk=id)
    if request.method == "POST":
        Booking.delete()  # Delete the booking
        return redirect('booking_list')  # Redirect to the booking list page
    return render(request, 'delete_booking.html', {'Booking': Booking})

#----------Update Booking--------
def update_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_date = request.POST.get('date')
        new_time = request.POST.get('time')
        new_waste = request.POST.get('waste')
        new_quant = request.POST.get('quant')

        # Retrieve the booking using the ID
        booking_to_update = get_object_or_404(booking, id=booking_id)

        # Update the booking's date and time
        booking_to_update.date = new_date
        booking_to_update.time = new_time
        booking_to_update.waste_type = new_waste
        booking_to_update.quantity = new_quant
        booking_to_update.save()

        messages.success(request, "Booking updated successfully.")
        return redirect('booking_list') 




#------------Admin dashboard views

def is_admin(user):
    return user.is_staff  # Only staff members are allowed to access the admin dashboard

@user_passes_test(is_admin)
def dashboard(request):
    all_requests = booking.objects.all()

    for req in all_requests:
        # Get the most recent task for the booking
        task = AdminTask.objects.filter(request=req).order_by('assigned_at').first()

        # Assign the status to the request (booking)
        if task:
            req.status = task.status  # Assign status of the found task
        else:
            req.status = 'Pending'
    
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
            return redirect('dashboard')
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

