from django.db import models

class Producto(models.Model):
    Product_id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=255)
    unit_place = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    origins = models.CharField(max_length=255)
    sold_in_pack = models.BooleanField()
    quantity = models.CharField(max_length=255)
    class Meta:    
        db_table = 'Producto'

class Existencia(models.Model):
    Product_id = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True)
    units = models.IntegerField()
    umbal = models.IntegerField()
    class Meta:
        db_table = 'Existencia'

class Paquete_producto(models.Model):
    Producto_id = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True)
    Pack_price = models.IntegerField()
    units = models.IntegerField()
    class Meta:
        db_table = 'Paquete_producto'