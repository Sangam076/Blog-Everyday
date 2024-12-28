from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.formats import date_format
from django.views.generic import ListView, TemplateView, View

from .forms import (
    BlogPostForm,
    CommentForm,
    ProfileForm,
    PostForm,
    ReplyForm,
    UserCreationForm,
)
from .models import BlogPost, Comment, Profile, Reply


# User List View
def user_list(request):
    query = request.GET.get('q', '')
    users = User.objects.all()

    if query:
        users = users.filter(username__icontains=query)  # Adjust filters as needed

    return render(request, 'user_list.html', {'users': users})


# User Profile View
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = BlogPost.objects.filter(author=user)
    return render(request, 'user_profile.html', {'user': user, 'posts': posts})


# Profile View
@login_required
def profile_view(request, username=None):
    user = request.user if username is None else get_object_or_404(User, username=username)
    
    profile, created = Profile.objects.get_or_create(user=user)
    posts = BlogPost.objects.filter(author=user).order_by('-created_at')

    if request.method == 'POST' and request.user == user:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view', username=user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'posts': posts,
        'is_owner': request.user == user,
    }

    return render(request, 'profile_view.html', context)


# Update Post View
@login_required
def update_post(request, id):
    post = get_object_or_404(BlogPost, id=id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('profile_view_user', username=request.user.username)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'is_update': True,
        'post': post,
    }

    return render(request, 'create.html', context)


# Delete Post View
@login_required
def delete_post(request, id):
    post = get_object_or_404(BlogPost, id=id, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('profile_view', username=request.user.username)

    return render(request, 'delete_post_confirm.html', {'post': post})


# Home Page View
class HomeView(ListView):
    model = BlogPost
    template_name = "index.html"
    context_object_name = "posts"
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        category = self.request.GET.get('category')

        if name:
            queryset = queryset.filter(title__icontains=name)
        if category and category != "All Categories":
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogPost.CATEGORY_CHOICES
        return context


# Logout User View
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed after registration.')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# About Page View
class AboutView(TemplateView):
    template_name = "about.html"


# Contact Page View
class ContactView(TemplateView):
    template_name = "contact.html"


# Blog List View
class BlogListView(ListView):
    model = BlogPost
    template_name = "blog.html"
    context_object_name = "blogs"
    ordering = ["-created_at"]
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        category = self.request.GET.get('category')

        if name:
            queryset = queryset.filter(title__icontains=name)
        if category and category != "All Categories":
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogPost.CATEGORY_CHOICES
        return context


# Blog Detail View
@login_required(login_url='login')
def blog_detail(request, id):
    blog = get_object_or_404(BlogPost, id=id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment_id = request.POST.get('comment_id')
            if comment_id:
                comment = get_object_or_404(Comment, id=comment_id)
                Reply.objects.create(comment=comment, author=request.user, content=content)
            else:
                Comment.objects.create(blog=blog, author=request.user, content=content)
            return redirect('blog_detail', id=id)

    return render(request, 'blog_detail.html', {'blog': blog})


# Add Comment View
@login_required(login_url='login')
def add_comment(request, id):
    blog = get_object_or_404(BlogPost, id=id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(blog=blog, author=request.user, content=content)

    return redirect('blog_detail', id=id)


# Reply to Comment View
@login_required(login_url='login')
def reply_comment(request, blog_id, comment_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    parent_comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                blog=blog,
                author=request.user,
                content=content,
                parent=parent_comment
            )

    return redirect('blog_detail', id=blog_id)


# Create Post View
class CreatePostView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        form = PostForm()
        return render(request, 'create.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
        return render(request, 'create.html', {'form': form})
