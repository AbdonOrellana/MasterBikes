from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('registro_confirmacion/', views.registro_confirmacion_view, name='registro_confirmacion'),
    path('activar/<uidb64>/<token>/', views.activar, name='activar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('arriendo/', views.arriendo, name='arriendo'),
    path('orden_arriendo/<int:orden_id>/', views.orden_arriendo, name='orden_arriendo'),  # Ruta para mostrar el detalle de una orden de arriendo
    path('home/', views.home, name='home'),
    path('reparacion/', views.reparacion, name='reparacion'),
    path('reparacion_exito/', views.reparacion_exito, name='reparacion_exito'),
    path('catalogo/', views.catalogo_bicicletas, name='catalogo_bicicletas'),
    path('bicicletas/<int:id>/', views.detalles_bicicleta, name='detalles_bicicleta'),
    path('buscar_bicicletas/', views.buscar_bicicletas, name='buscar_bicicletas'),
    path('ordenes/', views.ver_todas_ordenes, name='ver_ordenes'),

]