from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
# from django.conf import settings
from django.db.models import Sum
import stripe

from .models import Carrito, CarritoItem, Pedido, Producto
from .serializers import CarritoSerializer, CarritoItemSerializer

#stripe.api_key = settings.STRIPE_SECRET_KEY

# Vistas para Carrito
class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    #permission_classes = [IsAuthenticated]

class CarritoItemViewSet(viewsets.ModelViewSet):
    queryset = CarritoItem.objects.all()
    serializer_class = CarritoItemSerializer
    #permission_classes = [IsAuthenticated]

# Procesar pagos con Stripe
@api_view(['POST'])
def procesar_pago(request):
    try:
        token = request.data.get('stripeToken')
        cantidad = request.data.get('cantidad')  # El total a pagar en centavos

        cargo = stripe.Charge.create(
            amount=cantidad,
            currency="usd",
            description="Compra en tienda virtual",
            source=token,
        )

        # Enviar notificación al usuario
        usuario = request.user
        enviar_notificacion_compra(usuario, cantidad / 100)

        return Response({"status": "pago realizado con éxito"})
    except stripe.error.StripeError as e:
        return Response({"error": str(e)})

# Enviar correo de confirmación de compra
def enviar_notificacion_compra(usuario, total):
    asunto = 'Confirmación de tu compra'
    mensaje = f"Hola {usuario.username},\n\nGracias por tu compra. El total es de {total}. Tu pedido estará disponible para recoger pronto."
    correo_destino = [usuario.email]
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, correo_destino)

# Reportes de ventas para el administrador
@api_view(['GET'])
# @user_passes_test(lambda u: u.is_superuser)  # type: ignore # Solo administradores
def reporte_ventas(request):
    total_ventas = Pedido.objects.filter(producto__tipo='P').aggregate(total=Sum('cantidad'))
    total_servicios = Pedido.objects.filter(producto__tipo='S').aggregate(total=Sum('cantidad'))
    
    return Response({
        "total_ventas_productos": total_ventas['total'],
        "total_servicios": total_servicios['total']
    })
