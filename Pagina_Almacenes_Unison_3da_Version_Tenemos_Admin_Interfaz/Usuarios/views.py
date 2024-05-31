from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from .forms import *
from .models import *

class CrearUsuario(CreateView):
    model = Cuenta
    form_class = FormularioUsuario
    template_name = 'crear_usuario.html'
    success_url = reverse_lazy('inicio_sesion')

    @transaction.atomic
    def form_valid(self, form):
        usuario = Usuarios.objects.create(
            Name=form.cleaned_data['username'],
            floor_id="default"
        )
        cuenta = form.save(commit=False)
        cuenta.User_Id = usuario
        cuenta.save()

        messages.success(self.request, f'Usuario {cuenta.username} creado correctamente')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('inicio_sesion')

class InicioSesionView(LoginView):
    template_name = 'iniciar_sesion.html'
    authentication_form = FormularioLogin

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        cuenta = Cuenta.objects.get(username=user.username)

        if cuenta.rol == 'Admin':
            return HttpResponseRedirect(reverse('portal_admin'))
        elif cuenta.rol == 'Intendencia':
            return HttpResponseRedirect(reverse('portal_intendencia'))
        else:
            return HttpResponseRedirect(reverse('pagina_principal'))

    def form_invalid(self, form):
        messages.error(self.request, 'Nombre de usuario o contraseña incorrectos.')
        return super().form_invalid(form)

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
