from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from django.utils.timezone import now
from django.contrib.auth.models import User
from user_app.models import UserProfileModel

# Create your models here.
class CategoryModel(models.Model):
    categoryName = models.CharField(max_length=100,unique=True)
    categoryImage = models.ImageField(upload_to='CategoryImage',null=True,blank=True)

    def __str__(self):
        return self.categoryName
    
class PostModel(models.Model):
    STATUS = (
        ('0','Draft'),
        ('1','Publish'),
    )
    SECTION = (
        ('Popular','Popular'),
        ('Recent','Recent'),
        ('Editors_Pick','Editors_Pick'),
        ('Trending','Trending'),
        ('Inspiration','Inspiration'),
        ('Latest_Post','Latest_Post'),
    )

    post_image = models.ImageField(upload_to='PostImages',null=True,blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = RichTextField()
    slug = models.SlugField(max_length=500,null=True,blank=True,unique=True)
    status = models.CharField(choices=STATUS,max_length=100)
    section = models.CharField(choices=SECTION,max_length=200)
    main_post = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User,related_name='blog_posts')

    def __str__(self):
        return self.title
    
def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = PostModel.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_reciver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_reciver,PostModel)

class TagModel(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class blogcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    user  = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    profile = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE,related_name='comments')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"sno:{self.sno} name:{self.user} comment:{self.comment}"

class contactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class subscriptionModel(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email