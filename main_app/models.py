from django.db import models

# Create your models here.

class Camera(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year_made = models.IntegerField()