from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('user_id', 'username', 'email',)
    list_filter = ('is_active', 'is_superuser')
    ordering = ('date_joined',)
    list_display = ('user_id','username', 'email', 'date_joined',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('user_id', 'username', 'email', )}),
        ('Permission', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('gender', 'age', 'occupation')},)
    )
admin.site.register(User, UserAdminConfig)

