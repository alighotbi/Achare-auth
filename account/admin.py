from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    # form = UserChangeForm
    # add_form = UserCreationForm
    list_display = ("phone_number",
                    "email",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    )
    list_filter = ("phone_number",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number',
                       'email',
                       'password1',
                       'password2',
                       'is_staff',
                       'is_active',
                       'is_superuser',)
        }),
    )

    fieldsets = (
        (None, {"fields": ("phone_number", "email", "password")}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    search_fields = ("phone_number", "email")
    ordering = ["phone_number"]

