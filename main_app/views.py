# TODO: Create upload views here
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

# include the following imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied # include this additional import
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# generics to start the rest views.
from rest_framework import generics, status, permissions
from .models import Camera, Film, Upload
from .serializers import CameraSerializer, UploadSerializer, FilmSerializer, UserSerializer

# Define the home view
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the camera-collector api home route!'}
        return Response(content)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Override create method
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
    })

# User Login returns the token, user data, and allows a token refresh.
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
# User Verification
class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)  # Fetch user profile
        refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
        return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
    })

# This makes it so it only shows the cameras you are logged in and can see.
class CameraList(generics.ListCreateAPIView):
    # queryset = Camera.objects.all() 
    # We are now not using the all version but the filter by owned by self version.
    serializer_class = CameraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # This ensures we only return cats belonging to the logged-in user
        user = self.request.user
        return Camera.objects.filter(user=user)

    def perform_create(self, serializer):
        # This associates the newly created cat with the logged-in user
        serializer.save(user=self.request.user)

class CameraDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Camera.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializers(instance)

        film_not_associated = Film.objects.exclude(id__in = instance.films.all())
        film_serializer = FilmSerializer(film_not_associated, many=True)

        return Response({
            'camera': serializer.data,
            'film_not_associated': film_serializer
        })
    
    def perform_update(self, serializer):
        cat = self.get_object()
        if cat.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this cat."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this cat."})
        instance.delete()

class UploadListCreate(generics.ListCreateAPIView):
    serializer_class = UploadSerializer

    def get_queryset(self):
        camera_id = self.kwargs['camera_id']
        return Upload.objects.filter(camera_id = camera_id)
    
    def preform_create(self, serializer):
        camera_id = self.kwargs['camera_id']
        camera =  Camera.objects.get(id = camera_id)
        serializer.save(camera=camera)
    


class UploadDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UploadSerializer
    lookup_field = 'id'

    def get_queryset(self):
        camera_id = self.kwargs['camera_id']
        return Upload.objects.filter(camera_id=camera_id)


class FilmList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    lookup_field = 'id'

class AddFilmToCamera(APIView):
    def post(self, request, camera_id, film_id):
        camera = Camera.objects.get(id=camera_id)
        film = Film.objects.get(id=film_id)
        camera.film.add(film)
        return Response({'message': f"Film {film.name} loaded into Camera {camera.name}"})
    
class RemoveFilmFromCamera(APIView):
    def post(self, request, camera_id, film_id):
        camera = Camera.objects.get(id=camera_id)
        film = Film.objects.get(id=film_id)
        camera.film.remove(film)
        return Response({'message': f'Film {film.name} removed from Camera {camera.name}'})