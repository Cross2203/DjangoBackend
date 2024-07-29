from rest_framework import viewsets, permissions, status
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CitaSerializer, DiagnosticoSerializer, PacienteSerializer, TratamientoSerializer, HistorialMedicoSerializer, RecetaSerializer, AntecedentesMedicosSerializer, ConsultaSerializer, RevisionOrganosSistemasSerializer, SignosVitalesSerializer, ExamenFisicoSerializer, HistorialMedicoFullSerializer
from .models import Cita, Diagnostico, Paciente, Tratamiento, HistorialMedico, Receta, AntecedentesMedicos, Consulta, RevisionOrganosSistemas, SignosVitales, ExamenFisico

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CitaSerializer

    @action(detail=False, methods=['get'], url_path='por-fecha')
    def get_citas_por_fecha(self, request):
        fecha_str = request.query_params.get('fecha', None)
        if fecha_str is not None:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                citas = Cita.objects.filter(fecha_hora__date=fecha).order_by('fecha_hora')
                serializer = CitaSerializer(citas, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Fecha inválida'}, status=400)
        return Response({'error': 'Fecha no proporcionada'}, status=400)
  
class DiagnosticoViewSet(viewsets.ModelViewSet):
  queryset = Diagnostico.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = DiagnosticoSerializer
  
class PacienteViewSet(viewsets.ModelViewSet):
  queryset = Paciente.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = PacienteSerializer
  
  @action(detail=False, methods=['get'])
  def total(self, request):
    total_pacientes = Paciente.objects.count()
    return Response({"total": total_pacientes})
  
class TratamientoViewSet(viewsets.ModelViewSet):
  queryset = Tratamiento.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = TratamientoSerializer
  
class HistorialMedicoViewSet(viewsets.ModelViewSet):
    queryset = HistorialMedico.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = HistorialMedicoSerializer

    def create(self, request, *args, **kwargs):
        paciente_id = request.data.get('paciente')
        
        try:
            paciente = Paciente.objects.get(id_patient=paciente_id)
        except Paciente.DoesNotExist:
            return Response({"paciente": ["Paciente with this ID does not exist."]}, status=status.HTTP_400_BAD_REQUEST)

        existing_historial = HistorialMedico.objects.filter(paciente=paciente).first()
        
        if existing_historial:
            serializer = self.get_serializer(existing_historial, data=request.data, partial=True)
        else:
            # Si no existe, creamos uno nuevo
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
      
    @action(detail=False, methods=['get'])
    def total(self, request):
      total_historiales = HistorialMedico.objects.count()
      return Response({"total": total_historiales})
      
class RecetaViewSet(viewsets.ModelViewSet):
  queryset = Receta.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = RecetaSerializer
  
class AntecedentesMedicosViewSet(viewsets.ModelViewSet):
  queryset = AntecedentesMedicos.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = AntecedentesMedicosSerializer
  
class ConsultaViewSet(viewsets.ModelViewSet):
  queryset = Consulta.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = ConsultaSerializer
  
class RevisionOrganosSistemasViewSet(viewsets.ModelViewSet):
  queryset = RevisionOrganosSistemas.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = RevisionOrganosSistemasSerializer
  
class SignosVitalesViewSet(viewsets.ModelViewSet):
  queryset = SignosVitales.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = SignosVitalesSerializer
  
class ExamenFisicoViewSet(viewsets.ModelViewSet):
  queryset = ExamenFisico.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = ExamenFisicoSerializer

class HistorialMedicoPacienteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        try:
            paciente = Paciente.objects.get(id_patient=pk)
            historial_medico = HistorialMedico.objects.filter(paciente=paciente)
            
            full_data = request.query_params.get('full_data', '').lower() == 'true'
            
            if full_data:
                serializer = HistorialMedicoFullSerializer(historial_medico, many=True)
            else:
                serializer = HistorialMedicoSerializer(historial_medico, many=True)
            
            return Response(serializer.data)
        except Paciente.DoesNotExist:
            return Response({"error": "Paciente not found"}, status=status.HTTP_404_NOT_FOUND)
        except HistorialMedico.DoesNotExist:
            return Response({"error": "Historial not found"}, status=status.HTTP_404_NOT_FOUND)
      
class CitasPacienteViewSet(viewsets.ViewSet):
    queryset = Cita.objects.none()
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        paciente = Paciente.objects.get(id_patient=pk)
        citas = Cita.objects.filter(paciente=paciente)
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)
      
class AntecedenteMedicoPacienteViewSet(viewsets.ViewSet):
    queryset = AntecedentesMedicos.objects.none()
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        paciente = Paciente.objects.get(id_patient=pk)
        antecedentes = AntecedentesMedicos.objects.filter(paciente=paciente)
        serializer = AntecedentesMedicosSerializer(antecedentes, many=True)
        return Response(serializer.data)
      
class ExamenFisicoPacienteViewSet(viewsets.ViewSet):
    queryset = ExamenFisico.objects.none()
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        try:
            paciente = Paciente.objects.get(id_patient=pk)
            examen_fisico = ExamenFisico.objects.filter(paciente=paciente)
            serializer = ExamenFisicoSerializer(examen_fisico, many=True)
            return Response(serializer.data)
        except Paciente.DoesNotExist:
            return Response({"error": "Paciente no encontrado"}, status=404)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Crear una copia mutable de request.data
        serializer = ExamenFisicoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RevisionOrganosSistemasPacienteViewSet(viewsets.ViewSet):
    queryset = RevisionOrganosSistemas.objects.none()
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        paciente = Paciente.objects.get(id_patient=pk)
        revision_organos = RevisionOrganosSistemas.objects.filter(paciente=paciente)
        serializer = RevisionOrganosSistemasSerializer(revision_organos, many=True)
        return Response(serializer.data)