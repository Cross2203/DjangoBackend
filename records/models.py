from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = AppUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Paciente(models.Model):
    id_patient = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    identification = models.CharField(max_length=20, unique=True, null=True, blank=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200, null=True, blank=True)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    motivo = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)
    
class TipoAntecedentesMedicos(models.Model):
    id_tipo_antecedentes = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    
class AntecedentesMedicos(models.Model):
    id_antecedentes = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo_antecedentes = models.ForeignKey(TipoAntecedentesMedicos, on_delete=models.CASCADE, default=1)
    descripcion = models.TextField(default='', null=True, blank=True)
    

class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

class Tratamiento(models.Model):
    id_tratamiento = models.AutoField(primary_key=True)
    descripcion = models.TextField(null=True, blank=True)
    duracion = models.CharField(max_length=50, null=True, blank=True)
    dosis = models.CharField(max_length=50, null=True, blank=True)
    frecuencia = models.CharField(max_length=50, null=True, blank=True)

class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True)
    fecha_receta = models.DateField(null=True, blank=True)
    medicamentos_recetados = models.TextField(null=True, blank=True)
    
class SignosVitales(models.Model):
    id_signos = models.AutoField(primary_key=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    presion_arterial_sistolica = models.IntegerField(null=True, blank=True)
    presion_arterial_diastolica = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    talla = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    saturacion_oxigeno = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    fecha_consulta = models.DateField(null=True, blank=True)
    motivo = models.TextField(null=True, blank=True)
    notas_medicas = models.TextField(default='', null=True, blank=True)
    
class HistorialMedico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True) 
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True, blank=True)
    signos_vitales = models.ForeignKey(SignosVitales, on_delete=models.CASCADE, null=True, blank=True)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, null=True, blank=True)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, null=True, blank=True)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id_historial:
            self.fecha_creacion = timezone.now()
        super(HistorialMedico, self).save(*args, **kwargs)
    
    
class OrganosSistemas(models.Model):
    id_organos = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    
class RevisionOrganosSistemas(models.Model):
    id_revision = models.AutoField(primary_key=True)
    fecha_revision = models.DateTimeField(auto_now_add=True) 
    tipo_organos = models.ForeignKey(OrganosSistemas, on_delete=models.CASCADE)
    descripcion = models.TextField(default='')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, default=1)
    url_revision = models.CharField(max_length=200, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id_revision:
            self.fecha_revision = timezone.now()
        super(RevisionOrganosSistemas, self).save(*args, **kwargs)

class AreasExamen(models.Model):
    id_area = models.AutoField(primary_key=True)
    tipo_area = models.CharField(max_length=100)

class ExamenFisico(models.Model):
    id_examen = models.AutoField(primary_key=True)
    fecha_examen = models.DateTimeField(auto_now_add=True) 
    tipo_area = models.ForeignKey(AreasExamen, on_delete=models.CASCADE)
    descripcion = models.TextField(default='')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, default=1)
    url_examen = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id_examen:
            self.fecha_examen = timezone.now()
        super(ExamenFisico, self).save(*args, **kwargs)
