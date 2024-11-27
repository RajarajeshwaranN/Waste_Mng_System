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
from django.db.models import Max, Subquery, OuterRef

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime





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
            if request.user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('index')  
            
        else:
            messages.error(request, 'Invalid password')
       

    return render(request, 'login.html')

@login_required
def booking_view(request):
    context = {
            'username': request.user.username,
            'email': request.user.email,
    }
    
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

        #-----sending email
        send_mail(
            'Booking Request Confirmation',
            f'Dear {name},\n\nYour booking request has been received.\n\nDetails:\nWaste Type: {waste_type}\nQuantity: {quantity}kg\nScheduled Date: {date}\nTime: {time}\n\nThank you for using our service.',
            'nrajarajeshwaran12@gmail.com.com',  # Sender email
            [email],  # Recipient email
            fail_silently=False,
        )

        return redirect('booking_list')

    # Render the form
    return render(request, 'booking.html', context)

#logout function---------
def logout_view(request):
    logout(request)
    return redirect('login') 



#-------Booking List of the user------
@login_required
def booking_list(request):
    #Booking_data = booking.objects.filter(email=request.user.email)

    user = request.user

    # Fetch the latest `assigned_at` and `status` from AdminTask for each Booking
    latest_admin_task = AdminTask.objects.filter(request_id=OuterRef('id')
        ).order_by('-assigned_at')

    # Annotate Booking table with latest status and assigned_at
    Booking_data = booking.objects.filter(email=request.user.email).annotate(
        latest_status=Subquery(latest_admin_task.values('status')[:1]),
        latest_assigned_time=Subquery(latest_admin_task.values('assigned_at')[:1])
        ).order_by('-latest_assigned_time')  # Sort by the latest `assigned_at`

    return render(request, 'booking_list.html', {'Booking_data': Booking_data})



@login_required
def delete_booking(request, id):
    # Ensure the booking exists and belongs to the current user
    Booking = get_object_or_404(booking, pk=id)
    if request.method == "POST":
        booking_email = Booking.email
        booking_name = Booking.name
        booking_id = Booking.id

        Booking.delete()  # Delete the booking
        send_mail(
            subject="Booking Cancellation Notification",
            message=f"Hello {booking_name},\n\nYour booking with ID {booking_id} has been cancelled successfully on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nDetails:\nWaste Type: {Booking.waste_type}\nQuantity: {Booking.quantity}kg\nScheduled Date: {Booking.date}\nTime: {Booking.time}\n\nIf you have any questions, please contact our support team.\n\nThank you!",
            from_email="no-reply@example.com",
            recipient_list=[booking_email],
            fail_silently=False,
        )
        return redirect('booking_list')  # Redirect to the booking list page
    return render(request, 'delete_booking.html', {'Booking': Booking})

#----------Update Booking--------
@login_required
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
    
    latest_assign_task = AdminTask.objects.filter(
        request_id=OuterRef('id')  # Assuming `AssignTask` has a foreign key to `Booking`
    ).order_by('-assigned_at')  # Order by latest `assigned_at`

    # Annotate the Booking model with the latest status and assigned_at time
    all_requests = booking.objects.annotate(
        latest_assigned_time=Subquery(latest_assign_task.values('assigned_at')[:1]),
        latest_status=Subquery(latest_assign_task.values('status')[:1])
    ).order_by('-latest_assigned_time')
    
    return render(request, 'admin_dashboard/dashboard.html', {'all_requests': all_requests})

@login_required
def users_list(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    users = User.objects.all()
    return render(request, 'admin_dashboard/users_list.html', {'users': users})

@login_required
def deactivate_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    try:
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()
        return redirect('users_list')
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

@user_passes_test(is_admin)
def assign_task(request, request_id):
    waste_request = get_object_or_404(booking, id=request_id)

    # admin_task = AdminTask.objects.filter(booking=booking).latest('assigned_at')


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

        # send_mail(
        #     f'Booking Status Updated: {waste_request.status}',
        #     f'Dear {waste_request.name},\n\nYour booking status has been updated to "{booking.status}".\n\nThank you.',
        #     'your_email@example.com',
        #     [waste_request.email],
        #     fail_silently=False,
        # )
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


#----------Email - notification ---
@receiver(post_save, sender=AdminTask)
def notify_status_update(sender, instance, **kwargs):
    """
    Sends an email notification to the user whenever the status of their booking is updated.
    """
    
    # Fetch the associated booking object
    booking_obj = instance.request  # Assuming `request` is the ForeignKey to `Booking`
    
    # Check if the status was updated (without FieldTracker)
    if kwargs.get('created', False) or instance.status:  # Ensuring the status is updated
        # Get the updated status and user's email
        updated_status = instance.status
        user_email = booking_obj.email  # Assuming `email` is a field in the `Booking` model

        # Construct and send an email notification
        send_mail(
            subject='Booking Status Updated',
            message=f"""
Hello {booking_obj.name},

Your booking with ID {booking_obj.id} has been updated. 
The current status is: {updated_status}.

Thank you for choosing our service!

Best regards,
Waste Management Team
            """,
            from_email='nrajarajeshwaran12@gmail.com',  
            recipient_list=[user_email],
            fail_silently=False,
        )

@receiver(post_save, sender=booking)
def notify_booking_update(sender, instance, created, **kwargs):
        
    subject = "Booking Modification Notification"
    message = f"Hello {instance.name},\n\nYour booking with ID {instance.id} has been updated.\n\nNew Details:\nDate: {instance.date}\nTime: {instance.time}\nQuantity: {instance.quantity}\nType: {instance.waste_type}\nStatus: {instance.status}\n\nThank you for using our service!"

    # Send email to the user
    send_mail(
        subject=subject,
        message=message,
        from_email='nrajarajeshwaran12@gmail.com',
        recipient_list=[instance.email],
        fail_silently=False,
    )
