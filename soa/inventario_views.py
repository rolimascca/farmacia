from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto
from .forms import  ProductoForm 


def inventario_service(request):
    return render(request, 'inventario_service.html')

#Listar productos
def productos_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos_list.html', {'productos': productos})
#Crear producto
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('productos_list')
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form})
#Editar producto
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('productos_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto_form.html', {'form': form, 'object': producto})
#Eliminar producto
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('productos_list')
    return render(request, 'producto_confirm_delete.html', {'object': producto})
