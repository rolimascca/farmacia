import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Venta, DetalleVenta, Producto, Cliente
from .forms import VentaForm 
from django.views.decorators.csrf import csrf_exempt


def ventas_list(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')
    return render(request, 'ventas_list.html', {'ventas': ventas})

def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        productos_data = request.POST.getlist('producto')
        cantidades_data = request.POST.getlist('cantidad')

        if form.is_valid():
            venta = form.save(commit=False)
            venta.total = 0  # Inicializamos total
            venta.save()

            total_venta = 0
            for prod_id, cant_str in zip(productos_data, cantidades_data):
                try:
                    producto = Producto.objects.get(pk=int(prod_id))
                    cantidad = int(cant_str)
                except (Producto.DoesNotExist, ValueError):
                    continue  # Saltar si datos inválidos

                if cantidad > producto.stock:
                    messages.error(request, f"No hay suficiente stock para {producto.nombre}.")
                    venta.delete()
                    return redirect('venta_create')

                precio_unitario = producto.precio
                subtotal = precio_unitario * cantidad

                detalle = DetalleVenta(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
                detalle.save()

                # Actualizar stock del producto
                producto.stock -= cantidad
                producto.save()

                total_venta += subtotal

            venta.total = total_venta
            venta.save()

            messages.success(request, "Venta creada correctamente.")
            return redirect('ventas_list')
        else:
            messages.error(request, "Error en el formulario.")
    else:
        form = VentaForm()

    # Enviar productos en formato JSON para el JS
    productos = Producto.objects.filter(stock__gt=0).values('id', 'nombre', 'precio', 'stock')
    productos_list = []
    for p in productos:
        p = dict(p)
        p['precio'] = float(p['precio'])
        productos_list.append(p)
    productos_json = json.dumps(productos_list)

    return render(request, 'venta_form.html', {'form': form, 'productos_json': productos_json})
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        # Al eliminar la venta, restauramos el stock
        for detalle in venta.detalles.all():
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        venta.delete()
        messages.success(request, "Venta eliminada correctamente.")
        return redirect('ventas_list')
    return render(request, 'venta_confirm_delete.html', {'object': venta})
