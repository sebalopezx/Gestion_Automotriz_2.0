from django.db import models
from django.contrib.auth.models import User, Group
from django.forms import CheckboxInput, DateField, DateTimeField, TimeField

from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

import string
import secrets

# Validadores
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator


# Create your groups here.
# Crear el grupo de clientes
# group_customer, created = Group.objects.get_or_create(name='Customer')
# Crear el grupo de recepcionistas
# group_recepcionist, created = Group.objects.get_or_create(name='Recepcionist')



# MODELO DE INDEX
class TitleHeader(models.Model):
    title_header = models.CharField(max_length=50, verbose_name='Título')

    class Meta:
        db_table = 'Título' 
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos' 

    def __str__(self):
        return f"{self.id}. {self.title_header}"

class Description(models.Model):
    title = models.CharField(max_length=50, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    description_small = models.CharField(max_length=255, verbose_name='Descripción pequeña')
    image_description = models.ImageField(upload_to='index/', default='index/mantenimiento.PNG', verbose_name='Imágen')
    have_constant = models.BooleanField(default=False, verbose_name='Tiene Constante')

    class Meta:
        db_table = 'Descripción' 
        verbose_name = 'Descripción'
        verbose_name_plural = 'Descripciones' 

    def points_value(self):
        from .models import ConfigConstant
        return ConfigConstant.objects.get(name='POINTS').value

    def __str__(self):
            return f"{self.id}. {self.title}"

class ConfigConstant(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Nombre')
    value = models.IntegerField(verbose_name='Valor')

    class Meta:
        # db_table = 'Constante' 
        verbose_name = 'Constante'
        verbose_name_plural = 'Constantes'

    def __str__(self):
        return f"{self.id}. {self.name} - {self.value}"

# MODELOS DE TABLAS

class Vehicle(models.Model):
    customer = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False,
                                verbose_name='Usuario')
    brand = models.CharField(max_length=50, verbose_name='Marca')
    model = models.CharField(max_length=50, verbose_name='Modelo')
    patent = models.CharField(max_length=6, verbose_name='Patente')
    year = models.PositiveIntegerField(default=0, verbose_name='Año')
    is_active = models.BooleanField(default=True, verbose_name='Disponible')
    
    class Meta:
        db_table = 'Vehículo' 
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos' 

    def __str__(self):
        return f"{self.brand.capitalize()} {self.model.capitalize()} ~ Patente: {self.patent} ~ cliente: {self.customer.first_name} {self.customer.last_name}"

class Workshop(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    address = models.CharField(max_length=100, verbose_name='Dirección')
    num_address = models.IntegerField(verbose_name='Número dirección')

    class Meta:
        db_table = 'Taller' 
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres' 

    def __str__(self):
        return f"{self.name}. {self.address} # {self.num_address}"

class Mechanic(models.Model):
    SPECIALTY_CHOICES = (
        ('Mecánico', 'Mecánico'),
        ('Eléctrico', 'Eléctrico'),
    )
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    phone = models.CharField(max_length=9,
                             verbose_name='Teléfono',
                             validators=[
                                MaxLengthValidator(limit_value=9)
                             ])
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, blank=True, verbose_name='Especialidad')
    image = models.ImageField(upload_to='mechanics/', default="mechanics/foto_personal.jpg", verbose_name='Imágen')
    is_active = models.BooleanField(default=True, verbose_name='Disponible')

    class Meta:
        db_table = 'Mecánico' 
        verbose_name = 'Mecánico'
        verbose_name_plural = 'Mecánicos' 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attention(models.Model):
    attention = models.TimeField(verbose_name='Atención')
    def formatted_attention(self):
        if self.attention.hour == 8:
            context = ('AM')
        else:
            context = ('PM') 
        return f"{self.attention.__format__('%H:%M')} {context}"
    
    class Meta:
        db_table = 'Atención' 
        verbose_name = 'Atención'
        verbose_name_plural = 'Atenciones' 

    def __str__(self):
        return f"{self.formatted_attention()}"

class Appointment(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, verbose_name='Data vehículo')
    attention = models.ForeignKey(Attention, on_delete=models.CASCADE, verbose_name='Atención')
    date_register = models.DateField(verbose_name='Fecha de cita')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación') # auto add: ingresa time automaticamente si no se ingresa manualmente
    date_finished = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalizado') # Blank , se puede dejar vacio para llenado posterior
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, verbose_name='Mecánico')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, verbose_name='Taller')
    description_customer = models.TextField(null=True, blank=True, verbose_name='Descripción de cliente')
    inprogress = models.BooleanField(default=False, verbose_name='En ejecución')
    completed = models.BooleanField(default=False, verbose_name='Completado')

    class Meta:
        db_table = 'Cita' 
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas' 

    def __str__(self):
        return f"Cita para vehículo: {self.vehicle} ~ Fecha de la Cita: {self.date_register.strftime('%d-%m-%Y')} a las {self.attention}"  

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    price = models.PositiveIntegerField(verbose_name='Precio')
    earn_points = models.PositiveIntegerField(verbose_name='Puntos por servicio')

    class Meta:
        db_table = 'Servicio' 
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios' 

    def formatted_price(self):
        return '${:,.0f} pesos'.format(self.price)
    
    def __str__(self):
        return f"{self.id}. {self.name} {self.formatted_price()}"


class VehicleStatus(models.Model):
    status = models.CharField(max_length=50, verbose_name='Estado')

    class Meta:
        db_table = 'Estado' 
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados' 

    def __str__(self):
        return f"{self.id}. {self.status}"

class Job(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name='Id_Cita')
    description_job = models.TextField(null=True, blank=True, verbose_name='Descripción trabajo')
    status = models.ForeignKey(VehicleStatus, on_delete=models.CASCADE, verbose_name='Id_Estado')

    class Meta:
        db_table = 'Trabajo' 
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Trabajos' 

    def __str__(self):
        return f"{self.appointment}"

class Work(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Id_Trabajo')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Id_Servicio')
    status_service = models.BooleanField(default=False, verbose_name='Estado de servicio')

    class Meta:
        db_table = 'Servicio por trabajo' 
        verbose_name = 'Servicio por trabajo'
        verbose_name_plural = 'Servicios por trabajo' 

    def __str__(self):
        return f"{self.id}. {self.job} {self.service} {self.status_service}"

class Point(models.Model):
    customer = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False,
                                verbose_name='Usuario')
    points = models.PositiveIntegerField(default=0, verbose_name='Puntos')
    
    class Meta:
        db_table = 'Punto' 
        verbose_name = 'Punto'
        verbose_name_plural = 'Puntos' 

    def __str__(self):
        return f" {self.customer} - Puntos: {self.points}"

class Coupon(models.Model):
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 null=False,
                                 blank=False,
                                 verbose_name='Usuario')
    coupon = models.CharField(max_length=50, unique=True, verbose_name='Cupón')
    valid = models.BooleanField(default=True, verbose_name='Válido')

    class Meta:
        db_table = 'Cupón' 
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones' 

    def __str__(self):
        return f"{self.coupon}"

    @staticmethod
    def generate_coupon_code():
        # Generar un código de cupón único
        alphabet = string.ascii_letters + string.digits
        coupon = ''.join(secrets.choice(alphabet) for i in range(8))  # Ajustar la longitud del cupon
        return coupon

class Checklist(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, verbose_name='Id_Trabajo')
    front_lights = models.BooleanField(default=False, verbose_name='Luces delanteras')
    rear_lights = models.BooleanField(default=False, verbose_name='Luces traseras')
    chassis = models.BooleanField(default=False, verbose_name='Chasis')
    cleaning = models.BooleanField(default=False, verbose_name='Limpieza')  
    extinguisher = models.BooleanField(default=False, verbose_name='Extinguidor')
    first_aid_kit = models.BooleanField(default=False, verbose_name='Botiquin')
    triangles = models.BooleanField(default=False, verbose_name='Triángulos')
    hydraulic_jack = models.BooleanField(default=False, verbose_name='Gato hidráulico')
    spare_wheel = models.BooleanField(default=False, verbose_name='Rueda repuesto')

    class Meta:
        db_table = 'Checklist' 
        verbose_name = 'Checklist'
        verbose_name_plural = 'Checklists' 

    def __str__(self):
        return f"""Checklist: 
                {self.id}.
                {self.front_lights}
                {self.rear_lights}
                {self.chassis} 
                {self.cleaning} 
                {self.extinguisher} 
                {self.first_aid_kit}
                {self.triangles}
                {self.hydraulic_jack}
                {self.spare_wheel}"""
