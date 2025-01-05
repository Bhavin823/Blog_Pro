from django import forms
from .models import PostModel
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["content"].required=False

    class Meta:
        model = PostModel
        fields = ['post_image','title','category','content','section','status']
        
        widgets = {
            "post_image" : forms.FileInput(
                attrs={"class":"form-control","required":True}
            ),
            "title" : forms.TextInput(
                attrs={"class":"form-control","placeholder":"Title","required":True}
            ),
            "category" : forms.Select(
                attrs={"class":"form-control","required":True}
            ),
            "content" : CKEditor5Widget(config_name="extends"),
            "section" : forms.Select(
                attrs={"class":"form-control","required":True}
            ),
            "status" : forms.Select(
                attrs={"class":"form-control","required":True}
            ),
        }
        
    def save(self,commit=True,user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()
        return post