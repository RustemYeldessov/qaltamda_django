from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from safedelete.admin import SafeDeleteAdmin, highlight_deleted

from .models import User

@admin.register(User)
class MyUserAdmin(SafeDeleteAdmin, UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'highlight_deleted_field')

    def highlight_deleted_field(self, obj):
        return highlight_deleted(obj)
    highlight_deleted_field.short_description = "Status"