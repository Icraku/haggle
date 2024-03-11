from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Customer(models.Model):
    id = models.BigAutoField(primary_key=True) # AutoField to prevent error.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.ImageField(upload_to='customer/avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, default="")
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payment_method_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name() # Return the customer name as the string representation of the object

class Merchant(models.Model):
    id = models.BigAutoField(primary_key=True) # AutoField to prevent error.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, default="")
    

    def __str__(self):
        return self.user.get_full_name() # Return the merchant name as the string representation of the object

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # AutoField to prevent error.
    name = models.CharField(max_length=100)  # Product name
    original_price = models.DecimalField(max_digits=10, decimal_places=2)  # Original price
    time = models.TimeField()  # Time for haggling
    date = models.DateField()  # Date for haggling
    margins = models.DecimalField(max_digits=5, decimal_places=2)  # haggling margins
    merchant_offer = models.DecimalField(max_digits=10, decimal_places=2)  # Last offer from merchant 
    created_at = models.DateTimeField(auto_now_add=True) # Date and time when the haggling was created

    def __str__(self):
        return self.name  # Return the product name as the string representation of the object

    