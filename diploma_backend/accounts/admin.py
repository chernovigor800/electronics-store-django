from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import ProfileUser


admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', )}),
    )
    list_display = ('username', 'is_staff', 'is_active', )
    search_fields = ('username', )


@admin.register(ProfileUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
            "pk", "user_username", "name", "surname", "patronymic", "phone", "email", "avatar"
            )
    list_display_links = "pk", "user_username"
    ordering = ("pk", )
    search_fields = ("name", )

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username'

