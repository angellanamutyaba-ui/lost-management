# add_user_management.py - Run this ONCE to add user management
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lost_management.settings')
django.setup()

from django.contrib.auth.models import User
from system.models import LostItem, FoundItem, Notification

def add_user_management():
    print("=" * 50)
    print("Adding User Management System")
    print("=" * 50)
    
    # Check if we need to add the user management views
    views_path = 'system/views.py'
    with open(views_path, 'r') as f:
        content = f.read()
    
    if 'def user_management' not in content:
        print("Adding user management functions to views.py...")
        
        # Code to append to views.py
        new_views_code = """

# ========== USER MANAGEMENT FUNCTIONS ==========
@staff_member_required
def user_management(request):
    \"\"\"Admin page to manage all users\"\"\"
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
    \"\"\"Activate or deactivate a user\"\"\"
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
    \"\"\"Make a user staff member\"\"\"
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
    \"\"\"Delete a user account\"\"\"
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
    \"\"\"View user details\"\"\"
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
"""
        
        with open(views_path, 'a') as f:
            f.write(new_views_code)
        print("✅ Views updated")
    else:
        print("⏩ Views already have user management")
    
    # Update urls.py
    urls_path = 'system/urls.py'
    with open(urls_path, 'r') as f:
        content = f.read()
    
    if 'user-management/' not in content:
        print("Adding URLs to urls.py...")
        
        new_urls = """
    # User Management URLs
    path('user-management/', views.user_management, name='user_management'),
    path('user-management/toggle/<int:id>/', views.toggle_user_status, name='toggle_user_status'),
    path('user-management/make-staff/<int:id>/', views.make_staff, name='make_staff'),
    path('user-management/delete/<int:id>/', views.delete_user, name='delete_user'),
    path('user-management/detail/<int:id>/', views.user_detail, name='user_detail'),
"""
        
        # Find the urlpatterns list and insert before the last bracket
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if ']' in line and 'urlpatterns' in str(new_lines[-2:]):
                # Insert before the closing bracket
                new_lines.insert(-1, new_urls)
                break
        
        with open(urls_path, 'w') as f:
            f.write('\n'.join(new_lines))
        print("✅ URLs updated")
    else:
        print("⏩ URLs already have user management")
    
    # Create user_management.html
    print("Creating user_management.html...")
    user_mgmt_html = '''{% extends 'base.html' %}

{% block content %}
<style>
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
</style>

<div class="container mt-4">
    <div class="card shadow">
        <div class="card-header bg-primary text-white">
            <h3><i class="bi bi-people-fill"></i> User Management</h3>
        </div>
        <div class="card-body">
            <div class="row mb-4 g-3">
                <div class="col-md-3"><div class="stat-box"><h2>{{ total_users }}</h2><p>Total Users</p></div></div>
                <div class="col-md-3"><div class="stat-box" style="background:#28a745"><h2>{{ active_users }}</h2><p>Active</p></div></div>
                <div class="col-md-3"><div class="stat-box" style="background:#ffc107;color:#333"><h2>{{ staff_users }}</h2><p>Staff</p></div></div>
                <div class="col-md-3"><div class="stat-box" style="background:#dc3545"><h2>{{ inactive_users }}</h2><p>Inactive</p></div></div>
            </div>
            
            <div class="mb-3"><input type="text" id="search" class="form-control" placeholder="Search users..."></div>
            
            <div class="table-responsive">
                <table class="table table-hover" id="userTable">
                    <thead class="table-dark"><tr><th>Username</th><th>Email</th><th>Lost</th><th>Found</th><th>Status</th><th>Role</th><th>Actions</th></tr></thead>
                    <tbody>
                        {% for user in users %}
                        <tr>
                            <td><a href="{% url 'user_detail' user.id %}">{{ user.username }}</a></td>
                            <td>{{ user.email|default:"-" }}</td>
                            <td>{{ user.lost_count }}</td>
                            <td>{{ user.found_count }}</td>
                            <td>{% if user.is_active %}<span class="badge bg-success">Active</span>{% else %}<span class="badge bg-danger">Inactive</span>{% endif %}</td>
                            <td>{% if user.is_staff %}<span class="badge bg-primary">Staff</span>{% else %}<span class="badge bg-secondary">User</span>{% endif %}</td>
                            <td>
                                {% if user != request.user %}
                                <a href="{% url 'toggle_user_status' user.id %}" class="btn btn-sm btn-warning">{% if user.is_active %}Deactivate{% else %}Activate{% endif %}</a>
                                <a href="{% url 'delete_user' user.id %}" class="btn btn-sm btn-danger" onclick="return confirm('Delete?')">Delete</a>
                                {% else %}<span class="text-muted">You</span>{% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
<script>
document.getElementById('search').addEventListener('keyup', function() {
    let filter = this.value.toLowerCase();
    let rows = document.querySelectorAll('#userTable tbody tr');
    rows.forEach(row => { row.style.display = row.textContent.toLowerCase().includes(filter) ? '' : 'none'; });
});
</script>
{% endblock %}'''
    
    with open('templates/user_management.html', 'w') as f:
        f.write(user_mgmt_html)
    print("✅ user_management.html created")
    
    # Create user_detail.html
    print("Creating user_detail.html...")
    user_detail_html = '''{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow">
        <div class="card-header bg-primary text-white"><h3><i class="bi bi-person-circle"></i> {{ user_detail.username }}</h3></div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h5>Account Info</h5>
                    <p><strong>Email:</strong> {{ user_detail.email|default:"-" }}<br>
                    <strong>Joined:</strong> {{ user_detail.date_joined|date:"M d, Y" }}<br>
                    <strong>Status:</strong> {% if user_detail.is_active %}Active{% else %}Inactive{% endif %}<br>
                    <strong>Role:</strong> {% if user_detail.is_staff %}Staff{% else %}User{% endif %}</p>
                </div>
                <div class="col-md-6">
                    <h5>Statistics</h5>
                    <p><strong>Lost Items:</strong> {{ lost_count }}<br>
                    <strong>Found Items:</strong> {{ found_count }}<br>
                    <strong>Unread Notifications:</strong> {{ unread_notifications }}</p>
                </div>
            </div>
            <a href="{% url 'user_management' %}" class="btn btn-secondary">Back</a>
        </div>
    </div>
</div>
{% endblock %}'''
    
    with open('templates/user_detail.html', 'w') as f:
        f.write(user_detail_html)
    print("✅ user_detail.html created")
    
    # Update base.html to add Users link
    base_path = 'templates/base.html'
    with open(base_path, 'r') as f:
        content = f.read()
    
    if 'user-management' not in content:
        print("Adding Users link to navbar...")
        # Find the Dashboard link and add Users link after it
        content = content.replace(
            '<a class="nav-link" href="{% url \'dashboard\' %}">\n                        Dashboard\n                    </a>',
            '<a class="nav-link" href="{% url \'dashboard\' %}">\n                        Dashboard\n                    </a>\n\n                {% if user.is_staff %}\n                <li class="nav-item">\n                    <a class="nav-link" href="{% url \'user_management\' %}">\n                        <i class="bi bi-people-fill"></i> Users\n                    </a>\n                </li>\n                {% endif %}'
        )
        with open(base_path, 'w') as f:
            f.write(content)
        print("✅ Navbar updated")
    else:
        print("⏩ Navbar already has Users link")
    
    print("\n" + "=" * 50)
    print("✅ USER MANAGEMENT ADDED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNow run these commands:")
    print("git add .")
    print("git commit -m 'Add user management system'")
    print("git push origin master")
    print("\nThen visit: https://lost-management.onrender.com/user-management")

if __name__ == '__main__':
    add_user_management()