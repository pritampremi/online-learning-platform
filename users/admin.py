from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_student', 'is_instructor', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_instructor', 'email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_student', 'is_instructor')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
