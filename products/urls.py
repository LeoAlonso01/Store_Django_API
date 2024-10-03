from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarritoViewSet, CarritoItemViewSet, procesar_pago, reporte_ventas

router = DefaultRouter()
router.register(r'carrito', CarritoViewSet)
router.register(r'carrito-items', CarritoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pago/', procesar_pago, name='procesar_pago'),
    path('reporte-ventas/', reporte_ventas, name='reporte_ventas'),
]
