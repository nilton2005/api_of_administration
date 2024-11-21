from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Category, RFID
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .serializer import ProductSerializer, CategorySerializer, RFIDSerializer
from django.db.models import Count, Sum
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from rest_framework import status

# create view for the index page
# create a view for pruducts page
# create a view for the product detail page
# create a view for the cart page
# create a view for the checkout page
# create a view for the login page
# create a view for the registration page
# create a view for the profile page
# create a view dashboard page

# creating view api for to consume the api rest of the rfid
class IndexApi(APIView):
    def get(self, request):
        context = {
            'message': 'API en línea, listo para trabajar'
        }
        return Response(context)
    
    
# creating view api for to products of the rfid

class ProductApi(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

#creating view api for query for rfid

class ProductFilterRfid(APIView):
    def get(self, request):
        rfid_uid = request.GET.get('idNFC', None)
        if not rfid_uid:
            return Response({
                "error": "ingrese un idRFID válido"
            }, status=status.HTTP_400_BAD_REQUEST)
        products = Product.objects.filter(idNFC__id_tag=rfid_uid)
        if products.exists():
            serializer = ProductSerializer(products , many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "NO hay productos con este uidRFID"},
                status=status.HTTP_404_NOT_FOUND
            )


# creating view api for to product detail of the rfid

class ProductDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# creating view api for to category of the rfid

class CategoryApi(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

# creating view api for to category detail of the rfid

class CategoryDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

# creating view api for to UID of the rfid

class UIDApi(ListCreateAPIView):
    queryset = RFID.objects.all()
    serializer_class = RFIDSerializer
    lookup_field = 'id'

# creating view api for to UID detail of the rfid

class UIDDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = RFID.objects.all()
    serializer_class = RFIDSerializer
    lookup_field = 'id'

@csrf_exempt
def esp32_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rfid_uid = data.get('message')
            esp32_id = data.get('id_esp32')
            print(f"RFID UID recibido: {rfid_uid}\nID ESP32: {esp32_id}")
            created = RFID.objects.get_or_create(id_tag=rfid_uid)

            # guardando el id del esp32
            id_RFID = RFID.objects.filter(id_tag=rfid_uid).first()
            id_esp32 = id_RFID.id_esp32
            print("su esp32 es ==> ", id_esp32)
            if(id_esp32 == None):
                id_RFID.id_esp32 = esp32_id
                print("esto aqui")
                id_RFID.save()
            else:
                print("ya tiene un id de ESP32")

                  
            if (created == True):
                print(created)
                print("Nuevo RFID registrado y guardado")
            else:
                print("RFID ya existe, restaré el producto")
                try:
                    idTagRFID = get_object_or_404(RFID, id_tag = rfid_uid)
                    print(idTagRFID.id)
                    product = Product.objects.filter(idNFC=idTagRFID).first()
                    if product:
                        if(product.stock >= 2):
                            product.stock -= 10
                            product.save()
                            print(f"Nuevo stock de {product.name}: {product.stock}")
                        else: 
                            print("el producto  ya no tiene stock válido")
                            print(f"El stock de {product.name}: {product.stock}")
                    else:
                        return JsonResponse({'status': 'failed', 'message': 'Producto no encontrado'}, status=404)
                    
                except Product.DoesNotExist:
                    return JsonResponse({'status': 'failed', 'message': 'Producto no encontrado'}, status=404)
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

# her this
class AnalyticsApi(APIView):
    def get(self, request):
        period = request.query_params.get('period', 'daily')
        today = datetime.today()
        
        if period == 'daily':
            start_date = today - timedelta(days=1)
        elif period == 'weekly':
            start_date = today - timedelta(weeks=1)
        elif period == 'monthly':
            start_date = today - timedelta(days=30)
        else:
            return Response({'status': 'failed', 'message': 'Invalid period'}, status=400)
        
        entries = Product.objects.filter(created_at__gte=start_date).extra({'date': "date(created_at)"}).values('date').annotate(count=Count('id'))
        exits = Product.objects.filter(updated_at__gte=start_date).extra({'date': "date(updated_at)"}).values('date').annotate(count=Count('id'))
        
        data = {
            'entries': list(entries),
            'exits': list(exits)
        }
        
        return Response(data)
    #here for this

class CategoryAnalyticsApi(APIView):
    def get(self, request):
        categories = Category.objects.all().annotate(total_items=Sum('product__stock'))
        data = [{'category': category.name, 'total_items': category.total_items} for category in categories]
        return Response(data)
