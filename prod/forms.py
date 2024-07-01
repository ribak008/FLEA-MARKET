from django.forms import ModelForm
from .models import Producto

class PublicacionForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','categoria','imagen']
        
    