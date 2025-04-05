from django.db import models
from django.core.exceptions import ValidationError
from abc import abstractmethod

class ModeloBase(models.Model):
    """Clase abstracta con métodos comunes"""
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def validar_texto(self, campo, valor):
        """Valida que el texto contenga solo letras"""
        if not valor.replace(' ', '').isalpha():
            raise ValidationError(f"{campo} debe contener solo letras")

    @staticmethod
    def obtener_hora_actual():
        """Método estático para obtener hora actual"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M")

    @abstractmethod
    def obtener_info(self):
        """Método abstracto que debe ser implementado por las clases hijas (polimorfismo)"""
        pass

class Servicio(ModeloBase):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    
    def obtener_info(self):
        """Información básica del servicio (polimorfismo)"""
        return f"Servicio: {self.nombre}"
    
    def __str__(self):
        return self.nombre

class Instructor(Servicio):
    especialidad = models.CharField(max_length=100)
    experiencia = models.IntegerField()
    
    def obtener_info(self):
        """Información extendida del instructor (polimorfismo)"""
        return f"{super().obtener_info()} (Especialidad: {self.especialidad}, Experiencia: {self.experiencia} años)"

    @classmethod
    def obtener_experiencia(cls):
        """Método de clase para obtener la experiencia media de los instructores"""
        return cls.objects.aggregate(models.Avg('experiencia'))  # Método de clase para obtener información agregada

class Cliente(ModeloBase):
    documento = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)
    
    def obtener_info(self):
        """Información básica del cliente (polimorfismo)"""
        return f"Cliente: {self.nombres} {self.apellidos}"
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Etiqueta(Servicio):
    tipo = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    
    def obtener_info(self):
        """Información extendida de la etiqueta (polimorfismo)"""
        return f"{super().obtener_info()} - Tipo: {self.tipo}, Código: {self.codigo}"

    @classmethod
    def obtener_etiquetas_por_tipo(cls, tipo):
        """Método de clase para obtener todas las etiquetas de un tipo específico"""
        return cls.objects.filter(tipo=tipo)  # Método de clase para filtrar etiquetas por tipo

class Protocolo(Servicio):
    nivel = models.CharField(max_length=100)
    normativas = models.TextField()
    
    def obtener_info(self):
        """Información extendida del protocolo (polimorfismo)"""
        return f"{super().obtener_info()} - Nivel: {self.nivel}, Normativas: {self.normativas[:50]}..."  # Solo primeros 50 caracteres de las normativas
    
    @staticmethod
    def obtener_normativas_completas():
        """Método estático para obtener todas las normativas de los protocolos"""
        return Protocolo.objects.values_list('normativas', flat=True)  # Método estático para obtener todas las normativas

class Reserva(ModeloBase):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    notas = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')

    def obtener_info(self):
        return f"Reserva de {self.servicio.nombre} para {self.cliente.nombres} el {self.fecha}"
    
    def __str__(self):
        return f"Reserva de {self.servicio.nombre} para {self.cliente.nombres} el {self.fecha}"