from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category
from .models import Document


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    search_fields = ['name']
    list_per_page = 30


@admin.register(Document)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    search_fields = ['name', 'code']
    list_filter = ['category']
    list_per_page = 30
