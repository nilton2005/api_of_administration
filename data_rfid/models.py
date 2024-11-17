from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='categories_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class RFID(models.Model):
    id_tag = models.CharField(max_length=50, unique=True)
    id_esp32 = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    fecha_llegada = models.DateField(null=True, blank=True)
    fecha_asignado = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.id_tag

class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='producto_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)  # Protege la categoría
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    idNFC = models.ForeignKey(RFID, on_delete=models.SET_NULL, null=True, blank=True)  # NFC puede quedar como null


    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    img = models.ImageField(upload_to='users_images/', null=True, blank=True)

    def __str__(self):
        return self.name
class Transacction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ' - ' + self.product.name