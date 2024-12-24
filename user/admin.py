from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile

# Register your models here.
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
