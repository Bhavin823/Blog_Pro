from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # index page
    path('',views.INDEX,name='home'),

    # category
    path('category/',views.CategoryView,name='category'),
    path('postbycate/<str:categoryName>/',views.PostsByCategoryView,name='postbycat'),

    # post
    path('postdetail/<slug:post_slug>/',views.PostdetailView,name='postdetail'),

    # create Post
    path('create_post',views.create_post,name='create_post'),
    
    # comment
    path('postdetail/<slug:post_slug>/postcomment/', views.postcomment, name='postcomment'),
    
    # user
    path('signup/',views.signupView,name='signup'),
    path('signuphandle',views.handelSignup,name='handelsignup'),
    path('loginhandle',views.loginhandle,name='loginhandle'),
    path('logouthandle',views.logouthandle,name='logouthandle'),

    # search
    path('search',views.searchView,name='search'),
    
    # like
    path('like/<slug:post_slug>/', views.likeview, name='like_post'),

    # about
    path('about',views.about,name='about'),

    # contact
    path('contact',views.contact,name='contact'),
    path('add_contact',views.add_contact,name = 'add_contact'),
    
    # subscription
    path('subscribe',views.subscription,name='subscribe'),
    path('addsubscription',views.addsubscription,name='addsubscription'),

    # comingsoon
    path('comingsoon',views.comigsoon,name='comingsoon'),
]
