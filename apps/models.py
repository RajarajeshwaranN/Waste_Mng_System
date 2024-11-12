from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser



# Create your models here.
# class User(AbstractBaseUser):
#     email = models.EmailField(primary_key=True, unique=True)

#     # username = models.CharField(max_length=20) 
#     # password = models.CharField(max_length=10)
#     # confirm_password = models.CharField(max_length=10)
  


#     REQUIRED_FIELDS = []
#     USERNAME_FIELD = 'email'

    


class booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    mobile = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    address = models.TextField()
    waste_type = models.CharField(max_length=10)
    quantity = models.IntegerField()


    class Meta:
        db_table = 'booking'  # Use the existing `booking` table
        managed = False

    def __str__(self):
        return f"{self.user.name} - {self.date} at {self.time}"
    
class AdminTask(models.Model):
    STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    request = models.ForeignKey(booking, on_delete=models.CASCADE, related_name='admin_tasks')
    assigned_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assigned')
    notes = models.TextField(blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task for {self.request} - {self.status}"


# class WasteRequest(models.Model):
#     WASTE_TYPES = [
#         ('Plastic', 'Plastic'),
#         ('Metal', 'Metal'),
#         ('Organic', 'Organic'),
#         ('Electronics', 'Electronics'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="waste_requests")
#     waste_type = models.CharField(max_length=50, choices=WASTE_TYPES)
#     quantity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Quantity in kilograms")
#     scheduled_time = models.DateTimeField(help_text="Scheduled time for waste collection")
#     status = models.CharField(max_length=20, default="Pending")

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.waste_type} - {self.quantity}kg"
