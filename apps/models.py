from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=20) 
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=10)
    confirm_password = models.CharField(max_length=10)

    class Meta:
        db_table = 'user'  # match the table name in MySQL
        managed = False     # Django won’t create/alter this table


class booking(models.Model):
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
        return f"{self.name} - {self.date} at {self.time}"