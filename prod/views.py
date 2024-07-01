from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import PublicacionForm
from .models import Producto
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html',{
        'productos':productos
    })
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('signin')
            except User.DoesNotExist:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden'
            })

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{
        'form':AuthenticationForm
    })
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form':AuthenticationForm,
                'error':'usuario o password es incorrecto'
                })
        else:
            login(request, user)
            return redirect('home')
def detalle_pub(request,pub_id):
    producto = get_object_or_404(Producto,pk=pub_id)
    return render(request,'detalle_pub.html',{
        'producto':producto
    })
 
@login_required
def mis_pubs(request):
    productos = Producto.objects.filter(user=request.user)
    return render(request, 'mis_pubs.html',{
        'productos':productos
    })    
@login_required
def actualizar_pub(request,pub_id):
    if request.method == 'GET':
        producto = get_object_or_404(Producto,pk=pub_id)
        form = PublicacionForm(instance=producto)
        return render(request,'actualizar_pub.html',{
            'producto':producto,
            'form':form
        })
    else:
        try:
            producto = get_object_or_404(Producto,pk=pub_id)
            form = PublicacionForm(request.POST,instance=producto)
            form.save()
            return redirect('actualizar_pub',pub_id=producto.id)
        except ValueError:
            return render(request,'actualizar_pub.html',{
                'producto':producto,
                'form':form,
                'error':"Error al actualizar"
            })    
@login_required
def eliminar_pub(request,pub_id):
    producto = get_object_or_404(Producto,pk=pub_id,user=request.user)
    if request.method == 'POST':
        producto.delete()
        return redirect('home')
@login_required
def signout(request):
    logout(request)
    return redirect('home')
@login_required
def crear_publicacion(request):
    if request.method == 'GET':
        return render(request, 'publicar.html', {'form': PublicacionForm()})
    else:
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_publicacion = form.save(commit=False)
            nueva_publicacion.user = request.user
            nueva_publicacion.save()
            return redirect('home')
        else:
            return render(request, 'publicar.html', {
                'form': form,
                'error': 'Los datos no son válidos'
            })          
