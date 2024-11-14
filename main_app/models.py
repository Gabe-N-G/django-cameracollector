from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
PROC = (
    ('UPL', 'Upload'),
    ('DEV', 'Develop'),
    ('SCN', 'Scan'),
    ('PRT','Print')
)

FLM = (
    ('A', 'Analog'),
    ('D', 'Digital')
)

class Film(models.Model):
    type = models.CharField(
        max_length= 1,
        choices = FLM,
        default = FLM[0][0]
    )
    color = models.BooleanField()
    brand = models.CharField(max_length=20)
    name = models.CharField(max_length=100, default= None)
    speed = models.IntegerField(default= None)

    def __str__(self):
        return f"{self.type}, {self.name}"


class Camera(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year_made = models.IntegerField()
    
    films = models.ManyToManyField(Film)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    # makes all cameras delete if user is gone.

    def __str__(self):
        return self.name
    
class Upload(models.Model):
    date = models.DateField('Upload Date')
    process = models.CharField(
        max_length=3,
        choices = PROC,
        default = PROC[0][0]
    )

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)

    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_process_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']
