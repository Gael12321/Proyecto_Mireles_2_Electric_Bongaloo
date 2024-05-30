from django import forms
from .models import Producto

class FormularioProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['Name', 'unit_place', 'category', 'description', 'origins', 'sold_in_pack', 'quantity']
        widgets = {
            'sold_in_pack': forms.CheckboxInput(attrs={'id': 'id_sold_in_pack'}),
            'quantity': forms.NumberInput(attrs={'id': 'id_quantity'}),
        }

class FormularioTomarProducto(forms.Form):
    cantidad_a_tomar = forms.IntegerField(
        label='Cantidad a tomar',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la cantidad a tomar',
                'required': 'required',
            }
        )
    )

class FormularioAgregarProducto(forms.Form):
    cantidad_a_agregar = forms.IntegerField(
        min_value=1,
        label='Cantidad a agregar',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la cantidad a agregar',
                'required': 'required',
            }
        )
    )

class FormularioAgregarAlCarrito(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        label='Cantidad a agregar',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la cantidad a agregar',
                'required': 'required',
            }
        )
    )
