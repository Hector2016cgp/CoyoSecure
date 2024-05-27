from django.db import models

# Create your models here.

class Ubicacion(models.Model):

    SEGURIDAD_CHOICES = [
        ('0', 'segura'),
        ('1', 'insegura'),
        ('2', 'zona delictiva'),
    ]
    
    codigo_postal = models.CharField("Código postal", max_length=10, unique=False)
    nombre_ciudad = models.CharField("Nombre de la ciudad", max_length=50)
    nombre_colonia = models.CharField("Nombre de la colonia", max_length=70)
    seguridad_zona = models.CharField(
        "Seguridad de la zona", 
        max_length=1,
        choices=SEGURIDAD_CHOICES, 
        default='0'
    )

    class Meta:
        verbose_name = "Dato de seguimiento"
        verbose_name_plural = "Datos de seguimiento"

    def __str__(self):
        return self.codigo_postal


class Delito(models.Model):
    TIPO_DELITO = [
        ('0', 'robo'),
        ('1', 'asalto'),
        ('2', 'abuso'),
        ('3', 'venta de drogas'),
        ('4', 'homicidio'),
        ('5', 'secuestro'),
        ('6', 'feminicidio'),
    ]
    
    codigop_delito = models.ForeignKey(Ubicacion, on_delete=models.CASCADE) 
    delegacion_delito = models.CharField("Delegación del delito", max_length=30)
    calle_delito = models.CharField("Calle del delito", max_length=30)
    colonia_delito = models.CharField("Colonia del delito", max_length=30)
    tipo_delito = models.CharField(
        "Tipo de Delito", 
        max_length=1,
        choices=TIPO_DELITO, 
        default='0'
    )
    
    descripcion = models.TextField("Descripción del delito", blank=True) #La persona podrá agregar una descripción del delito.

    class Meta:
        verbose_name = "Registro de delito"
        verbose_name_plural = "Registros de delitos"

    def __str__(self):
        return self.codigop_delito.codigo_postal

class Delincuente(models.Model):

    codigop_delincuente = models.ForeignKey(Ubicacion,on_delete=models.CASCADE) 
    nombre_delincuente = models.CharField("Nombre del delincuente", max_length=40)
    proceso = models.CharField("¿Se encuentra en proceso el delincuente?", max_length=100)
    avatar = models.ImageField("Imagen del delincuente",upload_to='media/delincuente', blank = True, null = True) #Aqui se guardará la IMAGEN.
    descripcion_delincuente = models.TextField("Describe las características del delincuente", blank=True) #La persona podrá agregar una descripción del delito.
   
    class Meta:
        verbose_name = "Datos de delicuente"
        verbose_name_plural = "Datos de los delincuentes"

    def __str__(self):
        return self.codigop_delincuente.codigo_postal   