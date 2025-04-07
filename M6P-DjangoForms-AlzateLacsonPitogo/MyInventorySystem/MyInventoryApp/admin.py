from django.contrib import admin
from .models import Supplier, WaterBottle, Account

# Register your models here.
admin.site.register(Supplier)
admin.site.register(WaterBottle)
admin.site.register(Account)
