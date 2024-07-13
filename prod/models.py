from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    id_cat = models.IntegerField()
    nombre_cat = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nombre_cat

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=500)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="imagenes")
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    
    def __str__(self):
            return self.nombre + '- Por: ' + self.user.username
        

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='elementos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"      