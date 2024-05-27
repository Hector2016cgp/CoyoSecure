from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  


app_name = "ubicacion_app"

urlpatterns = [
    path('', views.InicioView.as_view(), name='Inicio'),
    path('ubicacion_actual/', views.ubicacion, name='ubicacion-actual'),
    path('registros-delitos/',views.ListAllZonas.as_view(),name='zonas_all'),
    path('registros-segura/', views.ListSegura.as_view(), name='zona_segura'),
    path('registros-insegura/', views.ListInsegura.as_view(), name='zona_insegura'),
    path('registros-delictiva/', views.ListDelictiva.as_view(), name='zona_delictiva'),
    # Clase para poder ver los delitos
    path("ver-delitos/<str:codigo_postal>/", views.DelitosPorCodigoPostalView.as_view(), name="delitos-registros"),
    path("update-zona/<str:codigo_postal>/", views.ZonaModUpdateView.as_view(), name = 'zona-modificada'),
    path("estado-seguridad/", views.estado_seguridad, name='estado-seguridad'),
    # Formulario para registrar un delito
    path('registrar-delito/', views.RegistrarDelitoView.as_view(), name='registrar_delito'),
    path('borrar-delito/<int:pk>/', views.DelitoDeleteView.as_view(), name="borrar-delito"), 
    path('registro-ratero/', views.RegistrarRateroView.as_view(), name='agregar-ratero'),
    path('ver-ratero/<str:codigo_postal>/', views.DelincuentesPorCodigoPostalView.as_view(), name='detalles-ratero'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)