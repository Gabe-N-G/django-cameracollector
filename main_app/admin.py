from django.contrib import admin
# import your models here
from .models import Camera, Film, Upload

# Register your models here
admin.site.register(Camera)
admin.site.register(Film)
admin.site.register(Upload)
