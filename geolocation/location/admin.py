from django.contrib import admin
from . models import Ubicacion
from . models import Delito
from . models import Delincuente


# Register your models here.

admin.site.register(Ubicacion)
admin.site.register(Delito)
admin.site.register(Delincuente)