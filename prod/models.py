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