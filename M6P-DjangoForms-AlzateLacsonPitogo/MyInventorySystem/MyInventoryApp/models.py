from django.db import models
from django.utils import timezone

class Account(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password

class Supplier(models.Model):
    name = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    created_at = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()

    def getName(self):
        return self.name
   
    def __str__(self):
        return "{} - {}, {} created at: {}".format(self.name, self.city, self.country, self.created_at)

class WaterBottle(models.Model):
    sku = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=100)
    mouth_size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    current_quantity = models.IntegerField()

    def __str__(self):
        return f"SKU: {self.sku}, Brand: {self.brand}, Mouth Size: {self.mouth_size}, " \
            f"Size: {self.size}, Color: {self.color}, Supplied by: {self.supplier.name}, " \
            f"Cost: {self.cost}, Quantity: {self.current_quantity}"

