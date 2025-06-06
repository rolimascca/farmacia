from django.urls import path
from .views import base, cliente_service, cliente_list, cliente_create, cliente_update, cliente_delete
from .inventario_views import productos_list, producto_create, producto_update, producto_delete
from .farmacias_view import ventas_list, venta_create, venta_delete

urlpatterns = [
    path('', base, name='base'),
    #Cliente Service
    path('cliente_service', cliente_service, name='cliente_service'),

    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', cliente_delete, name='cliente_delete'),

    #Inverario Service
    path('productos/', productos_list, name='productos_list'),
    path('productos/nuevo/', producto_create, name='producto_create'),
    path('productos/<int:pk>/editar/', producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', producto_delete, name='producto_delete'),


    path('ventas/', ventas_list, name='ventas_list'),
    path('ventas/nuevo/', venta_create, name='venta_create'),
    path('ventas/<int:pk>/eliminar/', venta_delete, name='venta_delete'),
]