from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileModel(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    GENDER = (
        ('M','Male'),
        ('F','Female'),
    )

    gender = models.CharField(choices=GENDER,max_length=200)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='Profile_image',null=True, blank=True)

    def __str__(self):
        return self.user.username
    