from django.db import models

# Create your models here.
PROC = (
    ('UPL', 'Upload'),
    ('DEV', 'Develop'),
    ('SCN', 'Scan'),
    ('PRT','Print')
)

class Camera(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year_made = models.IntegerField()

    def __str__(self):
        return self.name

class Upload(models.Model):
    date = models.DateField()
    process = models.CharField(
        max_length=3,
        choices = PROC,
        default = PROC[0][0]
    )

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)

    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_process_display()} on {self.date}"