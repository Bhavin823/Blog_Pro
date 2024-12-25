from django.shortcuts import render,redirect
from Blog_app.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from django.core.paginator import Paginator
from user_app.models import UserProfileModel
from django.utils.timezone import now
from django.db.models import F,Count
from dateutil.relativedelta import relativedelta
from .models import contactModel,subscriptionModel
# Create your views here.


def get_trending_post():
    one_month_ago = now().date() - relativedelta(months=1)  # Define the time frame as 1 month ago
    trending_posts = PostModel.objects.filter(date__gte=one_month_ago) \
        .annotate(comment_count=Count('comments',distinct=True))\
        .annotate(likes_count=Count('likes',distinct=True)) \
        .annotate(trend_score=F('views') + (2 * F('likes_count')) + (3 * F('comment_count'))) \
        .order_by('-trend_score')[:4]  # Sort by trend score in descending order
    return trending_posts



def BASE(request):
    
    return render(request,'Main/base.html')

def INDEX(request):
    # fetch posts data  according section from PostModel 
    # main section post
    main_post = PostModel.objects.filter(main_post=True,status=1)[0:1]
    
    # get trending post
    trending_posts = get_trending_post()
    # explore section posts
    programming_post = PostModel.objects.filter(category__categoryName='Programing')[:4]

    # Retrieve the 4 most popular posts
    popular_post = PostModel.objects.filter(status=1).order_by('-views')[:4]
    # Retrieve the 4 most recent posts
    recent_post = PostModel.objects.filter(status=1).order_by('-date')[:4]
    # specified section post
    editors_pick = PostModel.objects.filter(section='Editors_Pick',status=1).order_by('-id')
    trending_post = PostModel.objects.filter(section='Trending',status=1).order_by('-id')
    inspiration = PostModel.objects.filter(section='Inspiration',status=1).order_by('-id')[0:2]
    latest_post = PostModel.objects.filter(status=1).order_by('-date')[0:4]
    celebrate_post = PostModel.objects.filter(section='Latest_Post',status=1).order_by('-id')
    
    #fetch all category from categoryModel
    category = CategoryModel.objects.all()  

    context = {
        'popular_post': popular_post,
        'recent_post': recent_post,
        'main_post': main_post,
        'editors_pick' : editors_pick,
        'trending_post' : trending_posts,
        'inspiration' : inspiration,
        'latest_post' : latest_post,
        'category' : category,
        'celebrate_post' : celebrate_post,
        'programming_post':programming_post,
        
    }
    return render(request,'Main/index.html',context)

def CategoryView(request):
    
    # fetch all category from categoryModel for category page
    category = CategoryModel.objects.all()  

    # fetch post data  according section from PostModel for category page
    popular_post = PostModel.objects.filter(status=1).order_by('-views')[:4]
    celebrate_post = PostModel.objects.filter(section='Latest_Post',status=1).order_by('-id')

    # category pagination
    paginator = Paginator(category, 18)  # 18 categories per page
    # print("page:",paginator)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'category' : category,
        'popular_post' : popular_post,
        'celebrate_post' : celebrate_post,
        'page':page,
    }
    return render(request,'category.html',context)


def PostsByCategoryView(request,categoryName):
    # print("categoryName:",categoryName)

    category = CategoryModel.objects.get(categoryName=categoryName)
    
    # fetch Posts which have specified category for postsbycategory page
    postbycategory = PostModel.objects.all().filter(category=category,status=1)
    # print("postbycat",postbycategory[0].category)

    # fetch Posts which have section = "Popular" and specified category for postsbycategory page
    popularpostbycategory = PostModel.objects.all().filter(category=category,status=1).order_by('-views')[:4] 

    # print("popostbycat:",popularpostbycategory)

    # fetch all category from categoryModel for postsbycategory page
    category = CategoryModel.objects.all()

    paginator = Paginator(postbycategory, 3)  # 10 posts per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        
        'postbycategory' : postbycategory,
        'popularpostbycategory' : popularpostbycategory,
        'category' : category,
        'page' :page
    
    }

    return render(request,'postsbycategory.html',context)

def PostdetailView(request,post_slug):
    # print("postId:",post_slug)

    # fetch post which id same as postId
    postdetail = PostModel.objects.get(slug=post_slug,status=1)

    # fetch tag of post which id is given
    tagofpost = TagModel.objects.filter(post=postdetail)
    # print("tagofpost:",tagofpost)
    
    # fetch popular_post which post category as same as shown category
    popularpostbycategory = PostModel.objects.filter(category=postdetail.category,status=1).order_by('-views')[:4] 
    # print("popostbycat:",popularpostbycategory)

    # fetch all category from categoryModel
    category = CategoryModel.objects.all()

    # post views count
    postdetail.views = postdetail.views + 1
    postdetail.save()

    # comment section
    comment = blogcomment.objects.filter(post=postdetail,parent=None)
    # print("comments: ",comment)
    
    replies = blogcomment.objects.filter(post=postdetail).exclude(parent=None)
    # print("replies:",replies)

    comment_count = comment.count() + replies.count()


    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    # print("reply:",replyDict)

    # show post liked or not
    user = request.user
    liked = postdetail.likes.filter(id=user.id).exists()

    
    context = {
        
        'postdetail' : postdetail,
        'tagofpost' : tagofpost,
        'popularpostbycategory' : popularpostbycategory,
        'category' : category,
        'comments' : comment,
        'replyDict' : replyDict,
        'liked' : liked,
        'comment_count':comment_count,

    }
    return render(request,'postdetail.html',context) 

def postcomment(request,post_slug):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postsno = request.POST.get("postsno")
        # print("postno:",postsno)
        post = PostModel.objects.get(pk=postsno)
        parentsno = request.POST.get("parentsno")
        profile = UserProfileModel.objects.get(user=user)
        if parentsno == "":
            comment = blogcomment(comment=comment, user=user, post=post, profile=profile)
        else:
            parent = blogcomment.objects.get(sno=parentsno)
            comment = blogcomment(comment=comment, user=user, post=post, parent=parent, profile=profile)
        comment.save()
    return redirect("postdetail", post_slug=post.slug)

def signupView(request):
    return render(request,'loginsignup.html')

def handelSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            data = User.objects.all().filter(email=email) | User.objects.all().filter(username=username)
            if len(data)<=0:
                myuser = User.objects.create_user(username, email, password1)
                myuser.save()
                return redirect('home')
            else:   
                return render(request,'loginsignup.html',{'messagekey':"User Already Exists"})
        else:
            return render(request,'loginsignup.html',{'messagekey':"Password Does Not Match"})
    else:
        return HttpResponse('404 - Not Found')
    
def loginhandle(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)
        # print(user)

        if user is not None:
            login(request,user)
            # print("login successfully")
            return redirect('home')
        else:
            return render(request,'loginsignup.html',{'messagekey':" Inavalid Credentials !"})

    return HttpResponse('404 - Not Found')

def logouthandle(request):
    logout(request)
    # print(" user logout")
    return redirect('home')

def searchView(request):
    query = request.GET['query']
    # releted_post = PostModel.objects.all()
    if len(query) >= 78:
        releted_posts=PostModel.objects.none()
    else:
        releted_post_title = PostModel.objects.filter(title__icontains=query)
        releted_post_content = PostModel.objects.filter(content__icontains=query)
        releted_posts = releted_post_title.union(releted_post_content)
    
    if releted_posts.count() == 0:
        return render(request,'search.html')
    
    # print(releted_posts.count())
    context = {
        'releted_post' : releted_posts,
        'query' : query
    }
    return render(request,'search.html',context)
from django.contrib.auth.decorators import login_required

@login_required
def likeview(request,post_slug):
    if request.method == 'POST':
        postdetail = PostModel.objects.get(slug=post_slug)       
        user = request.user
        liked = postdetail.likes.filter(id=user.id).exists()

        if liked:
                postdetail.likes.remove(user)
                # print("user alredy liked post")
        else:
            postdetail.likes.add(user)
            # print("user liked post")

    return redirect("postdetail", post_slug=post_slug)


def profileView(request):
    return render(request,'profile.html')

def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')

def add_contact(request):
    if request.method == "POST":
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        text = request.POST.get('InputMessage')
        contat_form_detail = contactModel.objects.create(
            name=name,
            email=email,
            message=text
            )
        contat_form_detail.save()
        return render('contact.html')

def subscription(request):
    return render(request,'subscription.html')

def addsubscription(request):
    if request.method == "POST":
        email = request.POST.get('email')

        if subscriptionModel.objects.filter(email=email).exists():
            return render(request, 'subscription.html', {'messagekey': "Already Subscribed"})
        
        subscription = subscriptionModel.objects.create(email=email)
        subscription.save()

        
        return render(request, 'subscription.html', {'messagekey': "Subscribed Successfully"})