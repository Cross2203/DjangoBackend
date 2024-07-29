from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .get_file import get_s3_file_url
from .upload_file import upload_file_to_s3
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .storage import CustomS3Boto3Storage
import uuid
  
class UserRegister(APIView):
  permission_classes = [permissions.AllowAny]
  def post(self, request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user = serializer.create(request.data)
      if user:
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
  permission_classes = [permissions.AllowAny]
  authentication_classes = [SessionAuthentication]
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user = serializer.check_user(request.data)
      if user:
        login(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

@method_decorator(csrf_protect, name='dispatch')
class UserLogout(APIView):
    def post(self, request):
        print('CSRF Token in request:', request.META.get('CSRF_COOKIE', 'Not found'))
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
  permission_classes = [permissions.IsAuthenticated]
  authentication_classes = [SessionAuthentication]
  def get(self, request):
    serializer = UserSerializer(request.user)
    return Response({'user': serializer.data}, status=status.HTTP_200_OK)
  
class GetFileView(APIView):
    def get(self, request, folder_name, file_name, *args, **kwargs):
        file_url = get_s3_file_url(file_name, folder_name)
        return Response({'file_url': file_url}, status=status.HTTP_200_OK)
      
class UploadFileView(APIView):
    def post(self, request, folder_name, *args, **kwargs):
        file = request.FILES['file']
        file_url = upload_file_to_s3(file, folder_name)
        return Response({'file_url': file_url}, status=status.HTTP_201_CREATED)
      
@csrf_exempt
def upload_file(request, folder_name):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        unique_filename = f"{uuid.uuid4()}-{file.name}"
        
        storage = CustomS3Boto3Storage(folder=folder_name)
        
        file_name = storage.save(unique_filename, ContentFile(file.read()))
        
        file_url = storage.url(file_name)
        
        return JsonResponse({'message': 'Archivo subido exitosamente', 'url': file_url})
    
    return JsonResponse({'error': 'Método no permitido o archivo no proporcionado'}, status=405)
  
