from django import forms
from .models import Pedido, Detalles_Pedidos, Solicitud, Detalles_solicitud

class FormularioPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['order_date', 'description', 'total_amount', 'status']

class FormularioDetallePedido(forms.ModelForm):
    class Meta:
        model = Detalles_Pedidos
        fields = ['product_id', 'quantity', 'subtotal']

class FormularioSolicitud(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['request_date', 'description', 'total_amount', 'status']

class FormularioDetalleSolicitud(forms.ModelForm):
    class Meta:
        model = Detalles_solicitud
        fields = ['product_id', 'quantity', 'subtotal']
