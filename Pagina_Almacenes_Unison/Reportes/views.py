from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView, TemplateView, DetailView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from .models import Pedido, Detalles_Pedidos, Solicitud, Detalles_solicitud, User
from .forms import FormularioPedido, FormularioDetallePedido, FormularioSolicitud, FormularioDetalleSolicitud

class ListaPedidos(ListView):
    model = Pedido
    template_name = 'pedidos/lista_pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Usuario administrador ve todos los pedidos
            return Pedido.objects.all()
        else:
            # Otros usuarios ven solo sus propios pedidos
            return Pedido.objects.filter(user=user)

class DetallePedido(DetailView):
    model = Pedido
    template_name = 'pedidos/detalle_pedido.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido = self.get_object()
        context['detalles_pedido'] = Detalles_Pedidos.objects.filter(order=pedido)
        return context

class CrearPedido(CreateView):
    model = Pedido
    form_class = FormularioPedido
    template_name = 'pedidos/crear_pedido.html'
    success_url = reverse_lazy('lista_pedidos')
    
    def form_valid(self, form):
        pedido = form.save(commit=False)
        pedido.user = self.request.user
        pedido.save()
        return HttpResponseRedirect(self.success_url)

class EliminarPedido(DeleteView):
    model = Pedido
    success_url = reverse_lazy('lista_pedidos')
    template_name = 'pedidos/confirmar_eliminar.html'

class ListaSolicitudes(ListView):
    model = Solicitud
    template_name = 'solicitudes/lista_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Solicitud.objects.all()
        else:
            return Solicitud.objects.filter(user=user)

class DetalleSolicitud(DetailView):
    model = Solicitud
    template_name = 'solicitudes/detalle_solicitud.html'
    context_object_name = 'solicitud'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud = self.get_object()
        context['detalles_solicitud'] = Detalles_solicitud.objects.filter(request=solicitud)
        return context

class CrearSolicitud(CreateView):
    model = Solicitud
    form_class = FormularioSolicitud
    template_name = 'solicitudes/crear_solicitud.html'
    success_url = reverse_lazy('lista_solicitudes')
    
    def form_valid(self, form):
        solicitud = form.save(commit=False)
        solicitud.user = self.request.user
        solicitud.save()
        return HttpResponseRedirect(self.success_url)

class EliminarSolicitud(DeleteView):
    model = Solicitud
    success_url = reverse_lazy('lista_solicitudes')
    template_name = 'solicitudes/confirmar_eliminar.html'

class BorrarTodosReportesView(View):
    template_name = 'reportes/borrar_todos_reportes.html'

    def get(self, request):
        pedidos = Pedido.objects.all()
        solicitudes = Solicitud.objects.all()
        return render(request, self.template_name, {'pedidos': pedidos, 'solicitudes': solicitudes})

    def post(self, request):
        Pedido.objects.all().delete()
        Solicitud.objects.all().delete()
        return redirect('portal_admin')
