from django.contrib import admin
from .models import Apps, Dicty


@admin.register(Apps)
class AppsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'command']
    list_filter = ['id', 'name']
    sortable_by = ['id', 'name']
    list_display_links = ('id', 'name')


@admin.register(Dicty)
class DictyAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'value']

