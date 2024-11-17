from rest_framework import serializers
from .models import Product, Category, RFID

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RFIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFID
        fields = '__all__'

