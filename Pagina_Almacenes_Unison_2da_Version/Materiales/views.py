from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from datetime import datetime
from django.db import transaction
from itertools import groupby
from django.db.models import Sum 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, DetailView, TemplateView, View

from .models import Producto, Existencia, Paquete_producto
from .forms import FormularioAgregarProducto, FormularioProducto, FormularioTomarProducto, FormularioAgregarAlCarrito

class ListaProductos(ListView):
    model = Producto
    template_name = 'productos/lista_producto.html'
    context_object_name = 'productos'
    
class AñadirProducto(CreateView):
    model = Producto
    form_class = FormularioProducto
    template_name = 'productos/añadir_producto.html'
    success_url = reverse_lazy('lista_productos')
    
    def post(self, request, *args, **kwargs):
        form = FormularioProducto(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            Existencia.objects.create(
                Product_id=producto,
                units=form.cleaned_data['quantity'],
                umbal=form.cleaned_data['umbal']
            )
            return HttpResponseRedirect(reverse_lazy("lista_productos"))
        else:
            return render(request, 'productos/añadir_producto.html', {'form': form})

class EditarProducto(UpdateView):
    model = Producto
    template_name = 'productos/editar_producto.html'
    form_class = FormularioProducto
    success_url = reverse_lazy('lista_productos')

    @transaction.atomic
    def form_valid(self, form):
        try:
            producto = form.save()
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            print(f"Error al guardar los cambios: {e}")
            return super().form_invalid(form)

class AgregarProducto(FormView):
    template_name = 'productos/agregar_producto.html'
    form_class = FormularioAgregarProducto
    success_url = reverse_lazy('lista_productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = get_object_or_404(Producto, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        producto = self.get_context_data()['producto']
        cantidad_a_agregar = form.cleaned_data['cantidad_a_agregar']
        existencia = get_object_or_404(Existencia, Product_id=producto)
        existencia.units += cantidad_a_agregar
        existencia.save()
        return super().form_valid(form)

class TomarProductoView(TemplateView):  
    template_name = 'productos/tomar_producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = get_object_or_404(Producto, pk=self.kwargs['pk'])
        context['form'] = FormularioTomarProducto()
        return context

    def post(self, request, *args, **kwargs):
        form = FormularioTomarProducto(request.POST)
        if form.is_valid():
            producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
            cantidad_deseada = form.cleaned_data['cantidad_a_tomar']
            existencia = get_object_or_404(Existencia, Product_id=producto)

            if cantidad_deseada < 0:
                form.add_error('cantidad_a_tomar', 'La cantidad a tomar no puede ser negativa.')
                return self.render_to_response(self.get_context_data(form=form))

            if cantidad_deseada <= existencia.units:
                existencia.units -= cantidad_deseada
                existencia.save()
                if existencia.units <= existencia.umbal:
                    # Crear reporte si las unidades son menores o iguales al umbral
                    pass
                return HttpResponseRedirect(reverse_lazy('lista_productos') + '?taken=true')
            else:
                form.add_error('cantidad_a_tomar', 'La cantidad deseada es mayor a la cantidad disponible.')
        return self.render_to_response(self.get_context_data(form=form))

class EliminarProducto(DeleteView):
    model = Producto
    success_url = reverse_lazy('lista_productos')
    template_name = 'productos/confirmar_eliminar.html'
        

        
class VerProducto(DetailView):
    model = Producto
    template_name = 'productos/ver_producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 
    
