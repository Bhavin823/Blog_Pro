from django.contrib import admin
from user_app.models import *
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display=['firstname','lastname','gender','email','mobile','profile_image']

admin.site.register(UserProfileModel,UserProfileAdmin)