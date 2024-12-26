from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('profile',views.profileView, name='profile'),
    
    # profile_image
    path('profile_image_upload/', views.profile_image_upload, name='profile_image_upload'),

    path('update_personal_info/', views.update_personal_info, name='update_personal_info'),

    # update email
    path('update_email/', views.update_email,name='update_email'),

    # update contact
    path('update_contact/', views.update_contact, name='update_contact'),
]