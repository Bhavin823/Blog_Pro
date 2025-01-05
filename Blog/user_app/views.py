from django.shortcuts import render,redirect,get_object_or_404
from user_app.models import UserProfileModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Blog_app.models import PostModel
from Blog_app.forms import BlogPostForm


# Create your views here.
@login_required
def profileView(request):
    userprofile = UserProfileModel.objects.get(user=request.user) 
    userprofile.email = User.email
    userprofile.save() 
    context={
        'profile':userprofile,
    }
    return render(request,'profile.html',context)

@login_required
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

@login_required
def update_personal_info(request):
    profile = UserProfileModel.objects.get(user=request.user)
    if request.method == 'POST':
        profile.firstname = request.POST.get('firstname')
        profile.lastname = request.POST.get('lastname')
        profile.gender = request.POST.get('gender')
        profile.save()
        return redirect('profile')

@login_required
def update_email(request):
    user = request.user
    if request.method == "POST":
        new_email = request.POST.get('email')
        user.email = new_email
        user.save()
        return redirect('profile')

@login_required
def update_contact(request):
    profile = UserProfileModel.objects.get(user=request.user)
    if request.method == "POST":
        new_contact = request.POST.get('mobileNumber')
        profile.mobile = new_contact
        profile.save()
        return redirect('profile')
    

@login_required
def user_blogs(request):
    user = request.user
    blogs  = user.user_posts.all()
    context = {
        'blogs':blogs,
    }
    return render(request,'user_blogs.html',context)


@login_required
def edit_blog(request,post_slug):
    try:
        post = PostModel.objects.get(slug=post_slug,author=request.user)
    except PostModel.DoesNotExist:
        return redirect('user_blogs')
    if request.method == "POST":
        form = BlogPostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('user_blogs')
    else:
        form = BlogPostForm(instance = post)    
    return render(request,'edit_blog.html',{'form':form,'post':post})


@login_required
def delete_blog(request,post_slug):
    blog  = PostModel.objects.get(slug=post_slug)
    blog.delete()
    return redirect('user_blogs')
