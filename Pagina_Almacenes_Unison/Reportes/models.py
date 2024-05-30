from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    description = models.CharField(max_length=255)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=255)
    class Meta:
        db_table = 'Pedido'

class Detalles_Pedidos(models.Model):
    order = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    class Meta:
        db_table = 'Detalles_Pedidos'
        unique_together = ('order', 'product_id')

class Solicitud(models.Model):
    request_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField()
    description = models.CharField(max_length=255)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=255)
    class Meta:
        db_table = 'Solicitud'

class Detalles_solicitud(models.Model):
    request = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    class Meta:
        db_table = 'Detalles_solicitud'
        unique_together = ('request', 'product_id')
