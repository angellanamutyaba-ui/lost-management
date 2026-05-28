from django.db import models
from django.contrib.auth.models import User


class LostItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_lost = models.DateField()
    image = models.ImageField(upload_to='lost_images/', null=True, blank=True)

    # SYSTEM FIELDS
    is_claimed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FoundItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    location_found = models.CharField(max_length=100)
    date_found = models.DateField()
    image = models.ImageField(upload_to='found_images/', null=True, blank=True)

    # SYSTEM FIELDS
    is_claimed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    # Add these imports at the top of models.py
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

# Add these classes at the end of models.py

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('approval', 'Item Approved'),
        ('rejection', 'Item Rejected'),
        ('claim', 'Item Claimed'),
        ('match', 'Potential Match Found'),
        ('reminder', 'Reminder'),
        ('system', 'System Notification'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class AlertPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alert_preferences')
    email_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    match_alerts = models.BooleanField(default=True)
    approval_alerts = models.BooleanField(default=True)
    claim_alerts = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Alert preferences for {self.user.username}"