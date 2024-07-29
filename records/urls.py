from rest_framework import routers
from .api import CitaViewSet, DiagnosticoViewSet, PacienteViewSet, TratamientoViewSet, HistorialMedicoViewSet, RecetaViewSet, HistorialMedicoPacienteViewSet, AntecedentesMedicosViewSet, AntecedenteMedicoPacienteViewSet, CitasPacienteViewSet, ConsultaViewSet, SignosVitalesViewSet, ExamenFisicoViewSet, RevisionOrganosSistemasViewSet, ExamenFisicoPacienteViewSet, RevisionOrganosSistemasPacienteViewSet
from .reports import generar_pdf_historial
from django.urls import path, include
from . import views


router = routers.DefaultRouter()

router.register('api/citas', CitaViewSet)
router.register('api/diagnosticos', DiagnosticoViewSet)
router.register('api/pacientes', PacienteViewSet)
router.register('api/tratamientos', TratamientoViewSet)
router.register('api/historiales', HistorialMedicoViewSet)
router.register('api/recetas', RecetaViewSet)
router.register('api/antecedentes', AntecedentesMedicosViewSet)
router.register('api/consultas', ConsultaViewSet)
router.register('api/signosvitales', SignosVitalesViewSet)
router.register('api/examenfisico', ExamenFisicoViewSet)
router.register('api/revisionorganossistemas', RevisionOrganosSistemasViewSet)
router.register('api/pacientes/historiales', HistorialMedicoPacienteViewSet, basename='historial-paciente')
router.register('api/pacientes/citas', CitasPacienteViewSet, basename='citas-paciente')
router.register('api/pacientes/antecedentes', AntecedenteMedicoPacienteViewSet, basename='antecedente-paciente')
router.register('api/pacientes/examenfisico', ExamenFisicoPacienteViewSet, basename='examenfisico-paciente')
router.register('api/pacientes/revisionorganossistemas', RevisionOrganosSistemasPacienteViewSet, basename='revisionorganos-paciente')

urlpatterns = [
    path('register', views.UserRegister.as_view(), name='register'), 
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
    path('historial/pdf/<int:id_historial>/', generar_pdf_historial, name='generar_pdf_historial'),
    path('upload/<str:folder_name>/', views.upload_file, name='upload-file'),
    path('get-file/<str:folder_name>/<str:file_name>/', views.GetFileView.as_view(), name='get-file'),
    path('', include(router.urls)),
]