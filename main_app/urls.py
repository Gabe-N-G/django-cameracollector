from django.urls import path
# import Home view from the views file
from .views import Home, CameraList, CameraDetail # additional imports

urlpatterns = [
    path('', Home.as_view(), name='home'),
        # new routes below 
    path('cameras/', CameraList.as_view(), name='cat-list'),
    path('cameras/<int:id>/', CameraDetail.as_view(), name='cat-detail'),
]
