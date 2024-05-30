from django.db import models

# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class Usuarios(models.Model):
    User_Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    floor_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'Usuarios'

class Cuenta(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'Admin'
    INTENDENCIA = 'Intendencia'
    OTRO = 'Otro'

    ROL_CHOICES = [
        (ADMIN, 'Admin'),
        (INTENDENCIA, 'Intendencia'),
        (OTRO, 'Otro'),
    ]
    
    User_Id = models.OneToOneField(Usuarios, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=255, choices=ROL_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'Cuenta'

        
class Login(models.Model):
    User_Id = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    day = models.DateField()
    hour = models.TimeField()
    class Meta:
        db_table = 'Login'
        unique_together = ('User_Id', 'day', 'hour')

class Piso(models.Model):
    floor_id = models.CharField(max_length=255, primary_key=True)
    departament_name = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    class Meta:    
        db_table = 'Piso'