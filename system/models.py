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