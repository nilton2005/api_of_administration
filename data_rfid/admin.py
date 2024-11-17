from django.contrib import admin

# Register your models here.

from .models import Product, Category, RFID, User, Transacction

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(RFID)
admin.site.register(User)
admin.site.register(Transacction)
