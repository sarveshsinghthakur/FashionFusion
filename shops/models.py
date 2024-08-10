from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class products(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    desc = models.CharField(max_length=550)
    date = models.DateField()
    image = models.ImageField(upload_to="shops/image")
    price = models.IntegerField()
    
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    number = models.IntegerField()
    query = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name

class checkout(models.Model):
    order_number = models.AutoField(primary_key=True) 
    items_json = models.TextField()
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f'Order {self.order_number} by {self.name}'

class Tracker(models.Model):
    update_id = models.AutoField(primary_key=True)  
    order = models.ForeignKey(checkout, on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000,default="order has been placed")
    timestamp = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f'Order_id is {self.order} update_id is {self.update_id}'