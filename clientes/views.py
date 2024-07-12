from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from .forms import CustomUserCreationForm, ArriendoForm, ReparacionForm
from .models import Cliente, Arriendo, Bicicleta, Reparacion
from itertools import chain
from django.contrib.auth.decorators import login_required
from Carro.models import Orden as OrdenCompra
from django.db.models import Q


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta en MasterBikes'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            message = render_to_string('clientes/activacion_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            to_email = user.email

            email = EmailMessage(
                subject=mail_subject,
                body=message,
                to=[to_email]
            )
            email.content_subtype = "html"  # Especifica que el contenido es HTML
            email.send()

            return render(request, 'clientes/registro_confirmacion.html')

    else:
        form = CustomUserCreationForm()

    return render(request, 'clientes/registro.html', {'form': form})

def activar(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Cliente.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Cliente.DoesNotExist):
        return render(request, 'clientes/activacion_invalida.html', {'error': 'El enlace de activación es inválido o el usuario no existe.'})
    if user is not None and default_token_generator.check_token(user, token):   
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'clientes/activacion_invalida.html', {'error': 'El token de activación no es válido o ha expirado.'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Usar el campo de email para la autenticación
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'clientes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def arriendo(request):
    bicicletas = Bicicleta.objects.filter(disponible_para_arriendo=True)
    if request.method == 'POST':
        form = ArriendoForm(request.POST)
        if form.is_valid():
            arriendo = form.save(commit=False)
            arriendo.cliente = request.user
            arriendo.save()  # Guarda el objeto y calcula los costos en el método save()
            request.session['orden_id'] = arriendo.id
            return redirect('orden_arriendo', orden_id=arriendo.id)
        else:
            print(form.errors)  # Esto mostrará los errores de validación en la consola del servidor
        return render(request, 'clientes/arriendo.html', {'form': form, 'bicicletas': bicicletas})
    else:
        form = ArriendoForm()
        return render(request, 'clientes/arriendo.html', {'form': form, 'bicicletas': bicicletas})

@login_required
def orden_arriendo(request, orden_id):
    orden = get_object_or_404(Arriendo, id=orden_id)
    return render(request, 'clientes/orden_arriendo.html', {'orden': orden})

@login_required
def reparacion(request):
    if request.method == 'POST':
        form = ReparacionForm(request.POST)
        if form.is_valid():
            reparacion = form.save(commit=False)
            reparacion.cliente = request.user
            reparacion.save()
            reserva = form.cleaned_data['reserva_tecnico']
            reserva.esta_disponible = False
            reserva.save()
            return redirect('reparacion_exito')
    else:
        form = ReparacionForm()
    print(form.fields['reserva_tecnico'].queryset)  # Para depurar el queryset
    return render(request, 'clientes/reparacion.html', {'form': form})

def reparacion_exito(request):
    return render(request, 'clientes/reparacion_exito.html')
    
def registro_confirmacion_view(request):
    return render(request, 'clientes/registro_confirmacion.html')

def home(request):
    bicicletas = Bicicleta.objects.all()  # Obtén todas las bicicletas o filtra según necesites
    return render(request, 'clientes/home.html', {'bicicletas': bicicletas})

def catalogo_bicicletas(request):
    bicicletas = Bicicleta.objects.filter(disponible_para_venta=True,
                                          stock__gt=0)  # Ajustar el filtro según necesidad
    return render(request, 'clientes/catalogo_bicicletas.html', {'bicicletas': bicicletas})

def detalles_bicicleta(request, id):
    bicicleta = get_object_or_404(Bicicleta, pk=id)
    return render(request, 'clientes/detalle_bicicletas.html', {'bicicleta': bicicleta})

def buscar_bicicletas(request):
    query = request.GET.get('search')
    if query:
        resultados = Bicicleta.objects.filter(
            Q(modelo__icontains=query) | 
            Q(tipo__icontains=query) | 
            Q(marca__icontains=query),
            Q(disponible_para_venta=True) | Q(disponible_para_arriendo=True),
            stock__gt=0  # Asegura que solo bicicletas con stock positivo sean consideradas
        )
    else:
        resultados = Bicicleta.objects.none()  # Retorna un queryset vacío si no hay búsqueda

    return render(request, 'clientes/resultados_busqueda.html', {'resultados': resultados})

@login_required
def ver_todas_ordenes(request):
    # Obtener todas las órdenes generales
    ordenes = OrdenCompra.objects.filter(usuario=request.user).prefetch_related('items').order_by('-fecha_creacion')
    
    # Obtener órdenes específicas
    ordenes_compra = OrdenCompra.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    reparaciones = Reparacion.objects.filter(cliente=request.user).order_by('-fecha_creacion')
    arriendos = Arriendo.objects.filter(cliente=request.user).order_by('-fecha_inicio')
    
    context = {
        'ordenes': ordenes,
        'ordenes_compra': ordenes_compra,
        'reparaciones': reparaciones,
        'arriendos': arriendos
    }
    
    return render(request, 'Clientes/ordenes.html', context)