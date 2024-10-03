from rest_framework import serializers
from .models import Carrito, CarritoItem , Producto

class CarritoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoItem
        fields = '__all__'
        
class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Carrito
        fields = ['usuario','items']