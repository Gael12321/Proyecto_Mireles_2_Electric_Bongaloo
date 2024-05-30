from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.contrib import messages

from .forms import *
from .models import *
# Create your views here.

class CrearUsuario(CreateView):
    model = Cuenta
    form_class = FormularioUsuario
    template_name = 'crear_usuario.html'
    url_redirect = reverse_lazy('inicio_sesion')

    @transaction.atomic
    def form_valid(self, form):
        # Crear el objeto Usuario
        usuario = Usuarios.objects.create(
            Name=form.cleaned_data['username'],  # Usando username para el campo Name
            lastname=form.cleaned_data['username'],  # Usando username para el campo lastname
            floor_id="default"  # Este es solo un ejemplo, ajústalo según tus necesidades
        )

        # Crear el objeto Cuenta
        cuenta = form.save(commit=False)
        cuenta.User_Id = usuario
        cuenta.password = form.cleaned_data["password1"]
        cuenta.save()

        messages.success(self.request, f'Usuario {cuenta.username} creado correctamente')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('portal_admin')

class InicioSesionView(LoginView):
    template_name = 'iniciar_sesion.html'
    authentication_form = FormularioLogin

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        cuenta = Cuenta.objects.get(username=user.username)

        if cuenta.rol == 'Admin':
            return HttpResponseRedirect(reverse('portal_admin'))
        elif cuenta.rol == 'Intendencia':
            return HttpResponseRedirect(reverse('portal_intendencia'))
        else:
            return response

class CerrarSesionView(LogoutView):
    next_page = reverse_lazy('inicio_sesion')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ListaUsuario(ListView):
    model = Usuarios
    template_name = 'lista_usuario.html'
    context_object_name = 'usuarios'

class VerUsuario(UpdateView, DetailView):
    model = Usuarios
    template_name = 'ver_usuarios.html'
    context_object_name = 'usuario'
    fields = ['Name', 'lastname', 'floor_id']
    success_url = reverse_lazy('lista_usuario')

class EditarUsuario(UpdateView):
    model = Usuarios
    template_name = 'editar_usuario.html'
    fields = ['Name', 'lastname', 'floor_id']
    success_url = reverse_lazy('lista_usuario')

class EliminarUsuario(DeleteView):
    model = Usuarios
    template_name = 'eliminar_usuario_confirmar.html'
    success_url = reverse_lazy('lista_usuario')
