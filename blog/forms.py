from django import forms
from .models import BlogPost, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
            
            'author': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md'}),
        }

# forms.py

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={"cols": 80, "rows": 15, "class": "form-control"})
    )
    class Meta:
        model = BlogPost  
        fields = ['title', 'content', 'category', 'image'] 
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-lg',
                'rows': '3',
                'placeholder': 'Add a comment...'
            })
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded-lg',
                'rows': '2',
                'placeholder': 'Write a reply...'
            })
        }

# forms.py
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio', 'twitter', 'facebook', 'instagram', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }





class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio', 'twitter', 'facebook', 'instagram', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'w-full'}),
            'twitter': forms.URLInput(attrs={'class': 'w-full'}),
            'facebook': forms.URLInput(attrs={'class': 'w-full'}),
            'instagram': forms.URLInput(attrs={'class': 'w-full'}),
            'linkedin': forms.URLInput(attrs={'class': 'w-full'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'user' in self.fields:
            del self.fields['user']