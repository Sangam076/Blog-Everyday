from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomeView, AboutView, ContactView, BlogListView, CreatePostView
from . import views
from .views import register
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')), 
    path('register/', register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('profile_view/<str:username>/', views.profile_view, name='profile_view_user'),
    path('users/', views.user_list, name='user_list'), 
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('blog/<int:id>/', views.blog_detail, name='post_detail'),    
    path('', HomeView.as_view(), name='home'),               
    path('about/', AboutView.as_view(), name='about'),       
    path('blog/', BlogListView.as_view(), name='blog'),        
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:id>/add_comment/', views.add_comment, name='add_comment'),
    path('blog/<int:id>/reply_comment/', views.reply_comment, name='reply_comment'),
    path('create/', CreatePostView.as_view(), name='create'), 
    path('blog/<int:id>/update/', views.update_post, name='update_post'),
    path('blog/<int:id>/delete/', views.delete_post, name='delete_post'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
