from django.contrib import admin
from tengecash.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_favorite')
    list_editable = ('is_favorite', )
    list_filter = ('user', 'is_favorite')
