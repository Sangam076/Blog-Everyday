from django.contrib import admin
from .models import BlogPost, Comment, Reply, Profile, User

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

