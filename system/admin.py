from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import LostItem, FoundItem, Notification, AlertPreference

# Register LostItem
@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'date_lost', 'is_approved', 'is_claimed', 'created_at')
    list_filter = ('is_approved', 'is_claimed', 'date_lost')
    search_fields = ('name', 'description', 'location')
    list_editable = ('is_approved', 'is_claimed')
    actions = ['approve_items', 'mark_claimed']

    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)
    approve_items.short_description = "Approve selected items"

    def mark_claimed(self, request, queryset):
        queryset.update(is_claimed=True)
    mark_claimed.short_description = "Mark selected items as claimed"

# Register FoundItem
@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location_found', 'date_found', 'is_approved', 'is_claimed', 'created_at')
    list_filter = ('is_approved', 'is_claimed', 'date_found')
    search_fields = ('name', 'description', 'location_found')
    list_editable = ('is_approved', 'is_claimed')
    actions = ['approve_items', 'mark_claimed']

    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)
    approve_items.short_description = "Approve selected items"

    def mark_claimed(self, request, queryset):
        queryset.update(is_claimed=True)
    mark_claimed.short_description = "Mark selected items as claimed"

# Register Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')

# Register AlertPreference
@admin.register(AlertPreference)
class AlertPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'in_app_notifications', 'match_alerts')
    list_filter = ('email_notifications', 'in_app_notifications')

# Custom User Admin to show groups
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'groups')
    filter_horizontal = ('groups', 'user_permissions')

# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Make sure Groups is visible
admin.site.unregister(Group)
admin.site.register(Group)

# Customize admin site header
admin.site.site_header = "Lost Management System Admin"
admin.site.site_title = "Lost Management Admin"
admin.site.index_title = "Welcome to Lost Management System"