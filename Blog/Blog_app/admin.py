from django.contrib import admin
from Blog_app.models import *

# Register your models here.
class TagTublerInline(admin.TabularInline):
    model = TagModel

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName','id','categoryImage']

class PostAdmin(admin.ModelAdmin):
    inlines = [TagTublerInline]
    def likes_count(self,obj):
        return obj.likes.count()
    list_display = ['id','title','author','category','status','section','main_post','date','likes_count','views']
    list_editable = ['category','status','section','main_post']
    search_fields = ['title','author','section']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['sno','parent','user','post','timestamp']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','message']

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email']

admin.site.register(CategoryModel,CategoryAdmin)
admin.site.register(PostModel,PostAdmin)
admin.site.register(TagModel)
admin.site.register(blogcomment,CommentAdmin)
admin.site.register(contactModel,ContactAdmin)
admin.site.register(subscriptionModel,SubscriptionAdmin)
