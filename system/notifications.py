# system/notifications.py
from .models import Notification, AlertPreference

def create_notification(user, title, message, notification_type, link=None):
    """Create an in-app notification"""
    if not user or not user.is_authenticated:
        return None
    
    try:
        prefs = AlertPreference.objects.get(user=user)
        if notification_type in ['approval', 'rejection'] and not prefs.approval_alerts:
            return None
        if notification_type == 'claim' and not prefs.claim_alerts:
            return None
        if notification_type == 'match' and not prefs.match_alerts:
            return None
        if not prefs.in_app_notifications:
            return None
    except AlertPreference.DoesNotExist:
        pass
    
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link
    )


def notify_item_approved(item, is_lost=True):
    """Notify user when their item is approved"""
    item_type = "lost" if is_lost else "found"
    user = item.user
    
    if user:
        title = f"{'Lost' if is_lost else 'Found'} Item Approved"
        message = f"Your {item_type} item '{item.name}' has been approved and is now visible."
        create_notification(user, title, message, 'approval', '/dashboard/')


def notify_item_rejected(item, is_lost=True, reason=None):
    """Notify user when their item is rejected"""
    item_type = "lost" if is_lost else "found"
    user = item.user
    
    if user:
        title = f"{'Lost' if is_lost else 'Found'} Item Rejected"
        message = f"Your {item_type} item '{item.name}' was rejected. {reason if reason else 'Please check and resubmit.'}"
        create_notification(user, title, message, 'rejection')


def notify_item_claimed(item, is_lost=True, claimer=None):
    """Notify when an item is claimed"""
    item_type = "lost" if is_lost else "found"
    user = item.user
    
    if user:
        title = f"{'Lost' if is_lost else 'Found'} Item Claimed"
        message = f"Your {item_type} item '{item.name}' has been marked as claimed."
        create_notification(user, title, message, 'claim')