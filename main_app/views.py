# TODO: Create upload views here
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

# generics to start the rest views.
from rest_framework import generics
from .models import Camera, Film, Upload
from .serializers import CameraSerializer, UploadSerializer, FilmSerializer

# Define the home view
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the camera-collector api home route!'}
        return Response(content)

class CameraList(generics.ListCreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class CameraDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializers(instance)

        film_not_associated = Film.objects.exclude(id__in = instance.films.all())
        film_serializer = FilmSerializer(film_not_associated, many=True)

        return Response({
            'camera': serializer.data,
            'film_not_associated': film_serializer
        })

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