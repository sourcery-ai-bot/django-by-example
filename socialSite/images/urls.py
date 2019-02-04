from django.urls import path
from . import views

name_space = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
]
