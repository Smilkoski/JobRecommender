from django.contrib import admin

# Register your models here.
# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Job, Tag


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets
    list_display = ('username', 'email', 'is_staff', 'is_superuser')


admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Tag)