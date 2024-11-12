from rest_framework import serializers
from .models import Camera, Upload

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'
        read_only_fields = ('camera',)