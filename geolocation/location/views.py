
# Create your views here.
import json
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
import requests
from .forms import UbicacionForm, DelitoForm, DelincuenteForm
# Create your views here.

from django.views.generic import(
    ListView, #Recordar borrar las que no se estarán usando
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
    FormView
)

import requests
import json
from django.shortcuts import render

#Importacion de views

from .models import Ubicacion, Delito, Delincuente


def ubicacion(request):
    # Obtener la IP del usuario
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    
    # Obtener la geolocalización basada en IP
    res = requests.get('http://ip-api.com/json/'+ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)
    
    return render(request, 'templates-generales/ubicacion.html', {'data': location_data})

    

class InicioView(TemplateView):
    # vista que carga la pagian de incio
    template_name="templates-generales/inicio.html"

#1) Logica para listar todos los empleados.
class ListAllZonas(ListView):
    template_name = "templates-generales/registroTotal.html"
    paginate_by=6
    ordering = "codigo_postal"
    context_object_name = 'registro'

    # http://127.0.0.1:8000/listar-todo-empleados/?page=4, para poder ingresar a las distintas páginas ingresamos la anterior URL.

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')

        lista = Ubicacion.objects.filter(
            codigo_postal__icontains = palabra_clave
        )
        return lista

#View para poder filtrar la zaona segura.  
class ListSegura(ListView):
    template_name = "zonas-seguridad/segura.html"
    paginate_by=3
    ordering = "codigo_postal"
    context_object_name = 'segura'

    # http://127.0.0.1:8000/listar-todo-empleados/?page=4, para poder ingresar a las distintas páginas ingresamos la anterior URL.

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')

        lista = Ubicacion.objects.filter(
            codigo_postal__icontains = palabra_clave,
            seguridad_zona = '0'
        )
        return lista

#View para poder filtrar las zonas inseguras    
class ListInsegura(ListView):
    template_name = "zonas-seguridad/insegura.html"
    paginate_by=3
    ordering = "codigo_postal"
    context_object_name = 'insegura'

    # http://127.0.0.1:8000/listar-todo-empleados/?page=4, para poder ingresar a las distintas páginas ingresamos la anterior URL.

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')

        lista = Ubicacion.objects.filter(
            codigo_postal__icontains = palabra_clave,
            seguridad_zona = '1'
        )
        return lista
    
#View para poder filtrar zonasDelictivas.
class ListDelictiva(ListView):
    template_name = "zonas-seguridad/zonaDelictiva.html"
    paginate_by = 3
    ordering = "codigo_postal"
    context_object_name = 'delictiva'

    # http://127.0.0.1:8000/listar-todo-empleados/?page=4, para poder ingresar a las distintas páginas ingresamos la anterior URL.

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')

        lista = Ubicacion.objects.filter(
            codigo_postal__icontains = palabra_clave,
            seguridad_zona = '2'
        )
        return lista
    

# -------------------------------------------------------------------

class DelitosPorCodigoPostalView(DetailView):
    template_name = "templates-generales/delito.html"
    
    def get(self, request, codigo_postal):
        ubicacion = get_object_or_404(Ubicacion, codigo_postal=codigo_postal)
        delitos = Delito.objects.filter(codigop_delito=ubicacion)
        context = {
            'delitos': delitos,
            'ubicacion': ubicacion,
        }
        return render(request, self.template_name, context)
    

# --------------------------------------------------------------------

# Parte para agregar los forms de modificacion

class ZonaModUpdateView(UpdateView):
    model = Ubicacion
    template_name = "forms/zonaMod.html"
    context_object_name = "modificacion"
    fields = [
        'nombre_ciudad',
        'nombre_colonia',
        'seguridad_zona',
    ]
    success_url = reverse_lazy("ubicacion_app:Inicio")
    slug_field = 'codigo_postal'
    slug_url_kwarg = 'codigo_postal'

    # def form_valid(self, form):
    #     return super().form_valid(form)
    def get_success_url(self):
        return reverse('ubicacion_app:zona-modificada', kwargs={'codigo_postal': self.object.codigo_postal}) + '?success=true'

def estado_seguridad(request):
    codigo_postal = request.GET.get('codigo_postal')
    if codigo_postal:
        ubicacion = get_object_or_404(Ubicacion, codigo_postal=codigo_postal)
        seguridad = dict(Ubicacion.SEGURIDAD_CHOICES).get(ubicacion.seguridad_zona)
    else:
        seguridad = None

    return render(request, 'templates-generales/ubicacion.html', {'seguridad': seguridad})



#Vista para poder registar un delitos cometido. FUNCION DE ALTA IMPORTANCIA.

class RegistrarDelitoView(CreateView):
    model = Delito
    form_class = DelitoForm
    template_name = 'forms/registrar_delito.html'
    success_url = reverse_lazy('ubicacion_app:Inicio')

    def form_valid(self, form):
        return super().form_valid(form)
    

#opcion para eliminar registros

class DelitoDeleteView(DeleteView):
    model = Delito 
    template_name = "ubicacion_app/delete.html"  # Asegúrate de que la plantilla esté en la carpeta correcta
    success_url = reverse_lazy("ubicacion_app:zonas_all")  # Cambia esta URL al lugar correcto después de borrar

    def get_success_url(self):
        # Después de borrar el delito, puedes redirigir a una página específica, como la lista de delitos
        return reverse_lazy("ubicacion_app:zonas_all")

class DelitoDeleteView(DeleteView):
    model = Delito
    template_name = "borrarDelitos/delete.html"  # Asegúrate de que la plantilla esté en la carpeta correcta
    success_url = reverse_lazy("ubicacion_app:zonas_all")  # Cambia esta URL según sea necesario

    def get_success_url(self):
        # Después de borrar el delito, puedes redirigir a una página específica, como la lista de delitos
        return reverse_lazy("ubicacion_app:zonas_all")

# Apartado para poder agregar a los rateros por codigo postal

class RegistrarRateroView(CreateView):
    model = Delincuente
    form_class = DelincuenteForm
    template_name = 'infoDelincuente\delincuente_form.html'
    success_url = reverse_lazy('ubicacion_app:Inicio')

    def form_valid(self, form):
        return super().form_valid(form)
    

# class RaterosPorCodigoPostalView(DetailView):
#     model = Delincuente
#     template_name = 'detalles_ratero.html'
#     context_object_name = 'ratero'
#     slug_field = 'codigop_delincuente'
#     slug_url_kwarg = 'codigop_delincuente'

class DelincuentesPorCodigoPostalView(DetailView):
    template_name = "infoDelincuente/detalle_delito.html"
    
    
    def get(self, request, codigo_postal):
        ubicacion = get_object_or_404(Ubicacion, codigo_postal=codigo_postal)
        delincuentes = Delincuente.objects.filter(codigop_delincuente=ubicacion)
        context = {
            'delincuentes': delincuentes,
            'ubicacion': ubicacion,
        }
        return render(request, self.template_name, context)
    
    
# class DelincuentesEspecíficosView(DetailView):
#     template_name = "infoDelincuente/detalle_delito.html"
#     context_object_name = "ratero_especifico"

#     def get(self, request, codigo_postal):
#         ubicacion = get_object_or_404(Ubicacion, codigo_postal=codigo_postal)
#         delincuentes = Delincuente.objects.filter(codigop_delincuente=ubicacion)
#         context = {
#             'delincuentes': delincuentes,
#             'ubicacion': ubicacion,
#         }
#         success_url = reverse_lazy('ubicacion_app:Inicio')
#         return render(request, self.template_name, context)