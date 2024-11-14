from rest_framework import serializers
from .models import Camera, Upload, Film
from django.contrib.auth.models import User


# include User serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  # Ensures the password is hashed correctly
        )
        
        return user
class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'
        read_only_fields = ('camera',)

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

    films = FilmSerializer(many=True, read_only=True)
    # add user field to Cat serializer
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make the user field read-only