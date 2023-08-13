from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',"staff_name"',password1', 'password2')}
        ),
    )

    list_display = ("username", "staff_name","is_staff","is_active")
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (None, {'fields': ('username', 'password',"staff_name")}),
        ('Permissions', {'fields': ("groups","is_active",'is_staff',"is_superuser",)}),
    )

CustomUser = get_user_model()
admin.site.register(CustomUser,CustomUserAdmin)
