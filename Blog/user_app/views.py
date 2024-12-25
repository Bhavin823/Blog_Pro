from django.shortcuts import render,redirect
from user_app.models import UserProfileModel
from django.contrib.auth.models import User


# Create your views here.
def profileView(request):
    userprofile = UserProfileModel.objects.get(user=request.user)  
    
    context={
        'profile':userprofile,
    }
    return render(request,'profile.html',context)

def profile_image_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('profile_photo')  # Use request.FILES to get the uploaded file
        user = request.user
        profile = UserProfileModel.objects.get_or_create(user=user)[0]  # Create the profile if it doesn't exist
        if image:  # Check if a file was provided
            profile.profile_image = image
            profile.save()
            print("Image saved!")

    return redirect('profile')

def name_and_gender(request):
    if request.method == 'POST':
        user = request.user
        profile = UserProfileModel.objects.get(user=user)
        profile.firstname = request.POST.get('firstname')
        profile.lastname = request.POST.get('lastname')
        profile.gender = request.POST.get('gender')

        profile.save()

    return redirect('profile')