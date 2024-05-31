from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, EmailValidator

class UsuarioManager(BaseUserManager):
    def _create_user(self, username, email, nombres, apellidos, rol, edificio, piso, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            nombres=nombres,
            apellidos=apellidos,
            rol=rol,
            edificio=edificio,
            piso=piso,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, nombres, apellidos, rol, edificio, piso, password=None, **extra_fields):
        return self._create_user(username, email, nombres, apellidos, rol, edificio, piso, password, False, False, **extra_fields)

    def create_superuser(self, username, email, nombres, apellidos, rol, edificio, piso, password=None, **extra_fields):
        return self._create_user(username, email, nombres, apellidos, rol, edificio, piso, password, True, True, **extra_fields)

class Usuarios(models.Model):
    User_Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    floor_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'Usuarios'

class Cuenta(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        ADMIN = 'Admin', 'Administrador'
        INTENDENCIA = 'Intendente', 'Intendencia'
        OTRO = 'Otro', 'Otro'
    User_Id = models.OneToOneField(Usuarios, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField('Usuario', max_length=50, unique=True, validators=[MinLengthValidator(limit_value=6)])
    email = models.EmailField('Correo electrónico', unique=True, validators=[EmailValidator()])
    rol = models.CharField('Rol', max_length=12, choices=Rol.choices, default=Rol.OTRO)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'rol']

    objects = UsuarioManager()

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
