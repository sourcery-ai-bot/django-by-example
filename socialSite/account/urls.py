from django.urls import path
from . import views

urlpatterns = [
    # login views
    path('login/', views.user_login, name='login'),
]
