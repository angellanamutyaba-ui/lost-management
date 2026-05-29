from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

from .models import LostItem, FoundItem, Notification, AlertPreference
from .notifications import notify_item_approved, notify_item_rejected, notify_item_claimed


# HOME PAGE
def home(request):
    # Get counts for dashboard
    lost_count = LostItem.objects.filter(is_approved=True).count()
    found_count = FoundItem.objects.filter(is_approved=True).count()
    claimed_count = LostItem.objects.filter(is_approved=True, is_claimed=True).count() + \
                   FoundItem.objects.filter(is_approved=True, is_claimed=True).count()
    unclaimed_count = LostItem.objects.filter(is_approved=True, is_claimed=False).count() + \
                     FoundItem.objects.filter(is_approved=True, is_claimed=False).count()
    
    # Get recent items for display
    lost_items = LostItem.objects.filter(is_approved=True).order_by('-created_at')[:6]
    found_items = FoundItem.objects.filter(is_approved=True).order_by('-created_at')[:6]
    
    context = {
        'lost_items': lost_items,
        'found_items': found_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'claimed_count': claimed_count,
        'unclaimed_count': unclaimed_count,
        'query': '',
    }
    return render(request, 'home.html', context)


# LOGIN VIEW
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password!")
    
    return render(request, 'login.html')


# REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Create alert preferences for new user
            AlertPreference.objects.create(user=user)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    
    return render(request, 'register.html')


# LOGOUT
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# DASHBOARD
@login_required
def dashboard(request):
    query = request.GET.get('q')
    
    # Show different items based on user type
    if request.user.is_staff:
        lost_items = LostItem.objects.all().order_by('-created_at')
        found_items = FoundItem.objects.all().order_by('-created_at')
    else:
        lost_items = LostItem.objects.filter(is_approved=True).order_by('-created_at')
        found_items = FoundItem.objects.filter(is_approved=True).order_by('-created_at')
    
    # Search functionality
    if query:
        lost_items = lost_items.filter(name__icontains=query)
        found_items = found_items.filter(name__icontains=query)
    
    # Count statistics
    lost_count = lost_items.count()
    found_count = found_items.count()
    claimed_count = lost_items.filter(is_claimed=True).count() + found_items.filter(is_claimed=True).count()
    unclaimed_count = lost_items.filter(is_claimed=False).count() + found_items.filter(is_claimed=False).count()
    
    # Pending approvals for staff
    pending_approvals = 0
    if request.user.is_staff:
        pending_approvals = LostItem.objects.filter(is_approved=False).count() + \
                           FoundItem.objects.filter(is_approved=False).count()
    
    # Get unread notifications count
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    
    context = {
        'lost_items': lost_items,
        'found_items': found_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'claimed_count': claimed_count,
        'unclaimed_count': unclaimed_count,
        'query': query,
        'pending_approvals': pending_approvals,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'dashboard.html', context)


# ADD LOST ITEM
@login_required
def add_lost(request):
    if request.method == 'POST':
        LostItem.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            date_lost=request.POST.get('date_lost'),
            image=request.FILES.get('image'),
            is_approved=False,  # Needs admin approval
        )
        messages.success(request, "Lost item submitted for admin approval!")
        return redirect('dashboard')
    
    return render(request, 'add_lost.html')


# ADD FOUND ITEM
@login_required
def add_found(request):
    if request.method == 'POST':
        FoundItem.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            location_found=request.POST.get('location_found'),
            date_found=request.POST.get('date_found'),
            image=request.FILES.get('image'),
            is_approved=False,  # Needs admin approval
        )
        messages.success(request, "Found item submitted for admin approval!")
        return redirect('dashboard')
    
    return render(request, 'add_found.html')


# CLAIM LOST ITEM
@login_required
def claim_lost(request, id):
    item = get_object_or_404(LostItem, id=id, is_approved=True)
    
    if not item.is_claimed:
        item.is_claimed = True
        item.save()
        notify_item_claimed(item, is_lost=True, claimer=request.user)
        messages.success(request, f"'{item.name}' has been marked as claimed!")
    else:
        messages.warning(request, "This item has already been claimed!")
    
    return redirect('dashboard')


# CLAIM FOUND ITEM
@login_required
def claim_found(request, id):
    item = get_object_or_404(FoundItem, id=id, is_approved=True)
    
    if not item.is_claimed:
        item.is_claimed = True
        item.save()
        notify_item_claimed(item, is_lost=False, claimer=request.user)
        messages.success(request, f"'{item.name}' has been marked as claimed!")
    else:
        messages.warning(request, "This item has already been claimed!")
    
    return redirect('dashboard')


# DELETE LOST ITEM
@staff_member_required
def delete_lost(request, id):
    item = get_object_or_404(LostItem, id=id)
    item_name = item.name
    item.delete()
    messages.success(request, f"Lost item '{item_name}' deleted successfully!")
    return redirect('dashboard')


# DELETE FOUND ITEM
@staff_member_required
def delete_found(request, id):
    item = get_object_or_404(FoundItem, id=id)
    item_name = item.name
    item.delete()
    messages.success(request, f"Found item '{item_name}' deleted successfully!")
    return redirect('dashboard')


# APPROVE LOST ITEM
@staff_member_required
def approve_lost(request, id):
    item = get_object_or_404(LostItem, id=id)
    item.is_approved = True
    item.save()
    notify_item_approved(item, is_lost=True)
    messages.success(request, f"Lost item '{item.name}' has been approved!")
    return redirect('dashboard')


# REJECT LOST ITEM
@staff_member_required
def reject_lost(request, id):
    item = get_object_or_404(LostItem, id=id)
    item_name = item.name
    notify_item_rejected(item, is_lost=True)
    item.delete()
    messages.success(request, f"Lost item '{item_name}' has been rejected!")
    return redirect('dashboard')


# APPROVE FOUND ITEM
@staff_member_required
def approve_found(request, id):
    item = get_object_or_404(FoundItem, id=id)
    item.is_approved = True
    item.save()
    notify_item_approved(item, is_lost=False)
    messages.success(request, f"Found item '{item.name}' has been approved!")
    return redirect('dashboard')


# REJECT FOUND ITEM
@staff_member_required
def reject_found(request, id):
    item = get_object_or_404(FoundItem, id=id)
    item_name = item.name
    notify_item_rejected(item, is_lost=False)
    item.delete()
    messages.success(request, f"Found item '{item_name}' has been rejected!")
    return redirect('dashboard')


# NOTIFICATION VIEWS
@login_required
def notifications_view(request):
    """View all notifications"""
    notifications = Notification.objects.filter(user=request.user)
    
    if request.GET.get('mark_read'):
        notifications.update(is_read=True)
        messages.success(request, "All notifications marked as read!")
        return redirect('notifications')
    
    if request.GET.get('clear_all'):
        notifications.delete()
        messages.success(request, "All notifications cleared!")
        return redirect('notifications')
    
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def mark_notification_read(request, id):
    """Mark a single notification as read"""
    notification = get_object_or_404(Notification, id=id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.link or 'notifications')


@login_required
def alert_preferences(request):
    """Manage alert preferences"""
    prefs, created = AlertPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        prefs.email_notifications = request.POST.get('email_notifications') == 'on'
        prefs.in_app_notifications = request.POST.get('in_app_notifications') == 'on'
        prefs.match_alerts = request.POST.get('match_alerts') == 'on'
        prefs.approval_alerts = request.POST.get('approval_alerts') == 'on'
        prefs.claim_alerts = request.POST.get('claim_alerts') == 'on'
        prefs.save()
        messages.success(request, "Notification preferences updated!")
        return redirect('alert_preferences')
    
    return render(request, 'alert_preferences.html', {'prefs': prefs})

# ========== USER MANAGEMENT FUNCTIONS ==========
@staff_member_required
def user_management(request):
    """Admin page to manage all users"""
    from django.contrib.auth.models import User
    users = User.objects.all().order_by('-date_joined')
    
    for user in users:
        user.lost_count = LostItem.objects.filter(user=user).count()
        user.found_count = FoundItem.objects.filter(user=user).count()
        user.notification_count = Notification.objects.filter(user=user, is_read=False).count()
    
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'staff_users': users.filter(is_staff=True).count(),
        'inactive_users': users.filter(is_active=False).count(),
    }
    return render(request, 'user_management.html', context)


@staff_member_required
def toggle_user_status(request, id):
    """Activate or deactivate a user"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=id)
    
    if user == request.user:
        messages.error(request, "You cannot change your own status!")
        return redirect('user_management')
    
    user.is_active = not user.is_active
    user.save()
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User '{user.username}' has been {status}!")
    return redirect('user_management')


@staff_member_required
def make_staff(request, id):
    """Make a user staff member"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=id)
    
    if user == request.user:
        messages.error(request, "You cannot change your own staff status!")
        return redirect('user_management')
    
    user.is_staff = not user.is_staff
    user.save()
    role = "staff member" if user.is_staff else "regular user"
    messages.success(request, f"User '{user.username}' is now a {role}!")
    return redirect('user_management')


@staff_member_required
def delete_user(request, id):
    """Delete a user account"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=id)
    
    if user == request.user:
        messages.error(request, "You cannot delete your own account!")
        return redirect('user_management')
    
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' has been deleted!")
    return redirect('user_management')


@staff_member_required
def user_detail(request, id):
    """View user details"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=id)
    
    lost_items = LostItem.objects.filter(user=user).order_by('-created_at')
    found_items = FoundItem.objects.filter(user=user).order_by('-created_at')
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]
    
    context = {
        'user_detail': user,
        'lost_items': lost_items,
        'found_items': found_items,
        'notifications': notifications,
        'lost_count': lost_items.count(),
        'found_count': found_items.count(),
        'unread_notifications': Notification.objects.filter(user=user, is_read=False).count(),
    }
    return render(request, 'user_detail.html', context)

# ========== USER MANAGEMENT FUNCTIONS ==========
from django.contrib.auth.models import User
from django.http import JsonResponse

@staff_member_required
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})
