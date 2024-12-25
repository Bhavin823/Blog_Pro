from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('profile',views.profileView, name='profile'),
    path('profile_image_upload/', views.profile_image_upload, name='profile_image_upload')
]