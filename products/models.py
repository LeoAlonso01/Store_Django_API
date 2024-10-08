from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#clase categoria para la bd
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre
    
#clase Producto o Servicio
class Producto(models.Model):
    PRODUCTO = 'P'
    SERVICIO = 'S'
    TIPO_CHOICE = [
        (PRODUCTO, 'Producto'),
        (SERVICIO, 'Servicio')
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICE, default=PRODUCTO)
    
    def __str__(self):
        return f" Producto o Servicio con el nombre {self.nombre} con el precio  {self.precio} de tipo {self.tipo} "
    
# carriro e items

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)
    
    def __str__(self):
        return f"Cantidad {self.cantidad} x {self.producto.nombre}"
    
# Pedido
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    recogido = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Pedido de {self.cantidad} x {self.producto.nombre} el {self.fecha}"
    

    
