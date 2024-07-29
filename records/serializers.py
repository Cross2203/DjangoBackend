from rest_framework import serializers
from .models import Cita, Diagnostico, Paciente, Tratamiento, HistorialMedico, Receta, AntecedentesMedicos, Consulta, RevisionOrganosSistemas, SignosVitales, ExamenFisico
from django.contrib.auth import get_user_model, authenticate

UserModer = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserModer
    fields = '__all__'

  def create(self, clean_data):
    user_obj = UserModer.objects.create_user(email=clean_data['email'], 
                                             password=clean_data['password'])
    user_obj.username = clean_data['username']
    user_obj.save()
    return user_obj
  
class UserLoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()
  ##
  def check_user(self, clean_data):
    user = authenticate(username=clean_data['email'], 
                        password=clean_data['password'])
    if not user:
      raise serializers.ValidationError('Invalid credentials')
    return user
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserModer
    fields = ('email', 'username')

class CitaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cita
    fields = '__all__'
    
class DiagnosticoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Diagnostico
    fields = '__all__'
    
class PacienteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Paciente
    fields = '__all__'  
    
class TratamientoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tratamiento
    fields = '__all__' 
  def to_internal_value(self, data):
    for field in self.fields:
        if data.get(field) == '':
            data[field] = None
    return super().to_internal_value(data)
    
class ConsultaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Consulta
    fields = '__all__'
  def to_internal_value(self, data):
    for field in self.fields:
        if data.get(field) == '':
            data[field] = None
    return super().to_internal_value(data)
    
class RevisionOrganosSistemasSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionOrganosSistemas
        fields = '__all__'

    def to_internal_value(self, data):
        for field in self.fields:
            if data.get(field) == '':
                data[field] = None
        return super().to_internal_value(data)

    def create(self, validated_data):
        return RevisionOrganosSistemas.objects.create(**validated_data)
    
class SignosVitalesSerializer(serializers.ModelSerializer):
  class Meta:
    model = SignosVitales
    fields = '__all__'
    
  def to_internal_value(self, data):
    for field in self.fields:
        if data.get(field) == '':
            data[field] = None
    return super().to_internal_value(data)
    
class ExamenFisicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamenFisico
        fields = '__all__'

    def to_internal_value(self, data):
        for field in self.fields:
            if data.get(field) == '':
                data[field] = None
        return super().to_internal_value(data)

    def create(self, validated_data):
        return ExamenFisico.objects.create(**validated_data)
    
    
class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = '__all__'
    def to_internal_value(self, data):
        for field in self.fields:
            if data.get(field) == '':
                data[field] = None
        return super().to_internal_value(data)

 
    
class AntecedentesMedicosSerializer(serializers.ModelSerializer):
  class Meta:
    model = AntecedentesMedicos
    fields = '__all__'
    
class HistorialMedicoSerializer(serializers.ModelSerializer):
    paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())
    consulta = serializers.PrimaryKeyRelatedField(queryset=Consulta.objects.all())
    signos_vitales = serializers.PrimaryKeyRelatedField(queryset=SignosVitales.objects.all())
    diagnostico = serializers.PrimaryKeyRelatedField(queryset=Diagnostico.objects.all())
    tratamiento = serializers.PrimaryKeyRelatedField(queryset=Tratamiento.objects.all())
    receta = serializers.PrimaryKeyRelatedField(queryset=Receta.objects.all())

    class Meta:
        model = HistorialMedico
        fields = '__all__'

    def create(self, validated_data):
        return HistorialMedico.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
      
class HistorialMedicoFullSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer()
    consulta = ConsultaSerializer()
    signos_vitales = SignosVitalesSerializer()
    diagnostico = DiagnosticoSerializer()
    tratamiento = TratamientoSerializer()
    receta = RecetaSerializer()

    class Meta:
        model = HistorialMedico
        fields = '__all__'