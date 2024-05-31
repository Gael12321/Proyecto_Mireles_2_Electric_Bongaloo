from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required, user_passes_test

from .views import Portal_admin, Portal_intendencia

from Usuarios.views import (
    InicioSesionView, CerrarSesionView, ListaUsuario, CrearUsuario, VerUsuario, EditarUsuario, EliminarUsuario
)
from Materiales.views import (
    ListaProductos, AñadirProducto, AgregarProducto, VerProducto,
    EditarProducto, TomarProductoView, EliminarProducto
)
from Reportes.views import (
    ListaPedidos, DetallePedido, CrearPedido, EliminarPedido,
    ListaSolicitudes, DetalleSolicitud, CrearSolicitud, EliminarSolicitud, BorrarTodosReportesView
)


def es_admin(user):
    return user.rol == 'Admin'

def es_intendencia(user):
    return user.rol == 'Intendencia'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/admin/', user_passes_test(es_admin, login_url='/iniciar-sesion/')(Portal_admin.as_view()), name='portal_admin'),
    path('portal/', user_passes_test(es_intendencia, login_url='/iniciar-sesion/')(Portal_intendencia.as_view()), name='portal_intendencia'),
    path('', RedirectView.as_view(url='iniciar-sesion/')),
]

urlpatterns += [
    path('iniciar-sesion/', InicioSesionView.as_view(), name='inicio_sesion'),
    path('cerrar-sesion/', CerrarSesionView.as_view(), name='cerrar_sesion'),   
    path('lista-usuarios/', ListaUsuario.as_view(), name='lista_usuario'),
    path('crear-usuario/', CrearUsuario.as_view(), name='crear_usuario'),
    path('ver-usuario/<int:pk>/', VerUsuario.as_view(), name='ver_usuarios'),
    path('editar-usuario/<int:pk>/', EditarUsuario.as_view(), name='editar_usuario'),
    path('eliminar-usuario/<int:pk>/', EliminarUsuario.as_view(), name='eliminar_usuario'),
]

urlpatterns += [
    path('lista-materiales/', login_required(ListaProductos.as_view()), name='lista_materiales'),
    path('añadir-producto/', login_required(AñadirProducto.as_view()), name='añadir_producto'),
    path('agregar-producto/<int:pk>/', login_required(AgregarProducto.as_view()), name='agregar_producto'),
    path('editar-producto/<int:pk>/', login_required(EditarProducto.as_view()), name='editar_producto'),
    path('tomar-producto/<int:pk>/', login_required(TomarProductoView.as_view()), name='tomar_producto'),
    path('eliminar-producto/<int:pk>/', login_required(EliminarProducto.as_view()), name='eliminar_producto'),
    path('ver-producto/<int:pk>/', VerProducto.as_view(), name='ver_producto'),
]

urlpatterns += [
    path('lista-pedidos/', login_required(ListaPedidos.as_view()), name='lista_reportes'),
    path('detalle-pedido/<int:pk>/', DetallePedido.as_view(), name='detalle_pedido'),
    path('crear-pedido/', login_required(CrearPedido.as_view()), name='crear_pedido'),
    path('eliminar-pedido/<int:pk>/', login_required(EliminarPedido.as_view()), name='eliminar_pedido'),
    path('lista-solicitudes/', login_required(ListaSolicitudes.as_view()), name='lista_gastos'),
    path('detalle-solicitud/<int:pk>/', DetalleSolicitud.as_view(), name='detalle_solicitud'),
    path('crear-solicitud/', login_required(CrearSolicitud.as_view()), name='crear_solicitud'),
    path('eliminar-solicitud/<int:pk>/', login_required(EliminarSolicitud.as_view()), name='eliminar_solicitud'),
    path('borrar-todos-reportes/', BorrarTodosReportesView.as_view(), name='borrar_todos_reportes'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
