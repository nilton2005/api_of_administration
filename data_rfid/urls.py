from django.urls import path
from .views import esp32_data
from rest_framework.documentation import include_docs_urls
from . import views


urlpatterns = [
    #para recibir los datos del esp32
    path('api/rfid', esp32_data, name='rfid_receive'),

    # Esta url es para consumir la api rest
    path('api/', views.IndexApi.as_view(), name='api'),
    # for product
    path('api/productos', views.ProductApi.as_view(), name='api-productos'),
    path('api/producto/<int:id>', views.ProductDetailApi.as_view(), name='api-producto'),

    # for categories

    path('api/categorias', views.CategoryApi.as_view(), name='api-categorias'),
    path('api/categoria/<int:id>', views.CategoryDetailApi.as_view(), name="api-categoria"),

    # for UID RFID
    path('api/uid', views.UIDApi.as_view(), name='api-uid'),
    path('api/uid/<int:id>', views.UIDDetailApi.as_view(), name='api-uid-detail'),

    # for documentation
    path('api/doc', include_docs_urls(title='API RFID', description='API para el manejo de productos RFID')),

    # for analytics
    path('api/analytics', views.AnalyticsApi.as_view(), name='api-analytics'),

    # for category analytics
    path('api/category-analytics', views.CategoryAnalyticsApi.as_view(), name='api-category-analytics'),
    
]