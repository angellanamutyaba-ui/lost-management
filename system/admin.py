from django.contrib import admin
from .models import LostItem, FoundItem


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'date_lost', 'is_claimed')
    list_filter = ('is_claimed', 'date_lost')
    search_fields = ('name', 'description', 'location')


@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location_found', 'date_found', 'is_claimed')
    list_filter = ('is_claimed', 'date_found')
    search_fields = ('name', 'description', 'location_found')