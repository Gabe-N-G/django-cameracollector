from django.urls import path
# import Home view from the views file
from .views import Home, CameraList, CameraDetail, UploadListCreate, UploadDetail, FilmList, FilmDetail, AddFilmToCamera, RemoveFilmFromCamera, CreateUserView, LoginView, VerifyUserView # additional imports
# TODO: Make O-2-M views for UploadList/UploadDetail

urlpatterns = [   
    path('', Home.as_view(), name='home'),
        # new routes below 
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('cameras/', CameraList.as_view(), name='camera-list'),
    path('cameras/<int:id>/', CameraDetail.as_view(), name='camera-detail'),
    path('cameras/<int:camera_id>/uploads/', UploadListCreate.as_view(), name='upload-list'),
    path('cameras/<int:camera_id>/uploads/<int:id>', UploadDetail.as_view(), name='upload-detail'),
    path('film/', FilmList.as_view(), name='film-list'),
    path('film/<int:id>', FilmDetail.as_view(), name='film-list'),
    path('cameras/<int:camera_id>/add_toy/<int:film_id>/', AddFilmToCamera.as_view(), name='add-film-to-camera'),
    path('cameras/<int:camera_id>/remove_toy/<int:film_id>/', RemoveFilmFromCamera.as_view(), name='remove-film-from-camera'),
]

