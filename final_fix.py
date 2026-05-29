# final_fix.py - Run ONCE to fix all issues
import os

print("=" * 60)
print("🔧 FINAL FIX - Fixing all issues")
print("=" * 60)

# 1. Fix user_management.html
print("\n📝 Fixing user_management.html...")
with open('templates/user_management.html', 'w') as f:
    f.write('{% extends "base.html" %}\n')
    f.write('\n')
    f.write('{% block content %}\n')
    f.write('<div class="container mt-4">\n')
    f.write('    <div class="card shadow">\n')
    f.write('        <div class="card-header bg-primary text-white">\n')
    f.write('            <h3><i class="bi bi-people-fill"></i> User Management</h3>\n')
    f.write('        </div>\n')
    f.write('        <div class="card-body">\n')
    f.write('            <div class="row mb-4 g-3">\n')
    f.write('                <div class="col-md-3"><div class="alert alert-primary text-center"><h4>{{ total_users }}</h4><p>Total Users</p></div></div>\n')
    f.write('                <div class="col-md-3"><div class="alert alert-success text-center"><h4>{{ active_users }}</h4><p>Active</p></div></div>\n')
    f.write('                <div class="col-md-3"><div class="alert alert-warning text-center"><h4>{{ staff_users }}</h4><p>Staff</p></div></div>\n')
    f.write('                <div class="col-md-3"><div class="alert alert-danger text-center"><h4>{{ inactive_users }}</h4><p>Inactive</p></div></div>\n')
    f.write('            </div>\n')
    f.write('            <div class="table-responsive">\n')
    f.write('                <table class="table table-bordered">\n')
    f.write('                    <thead class="table-dark">\n')
    f.write('                        <tr><th>Username</th><th>Email</th><th>Lost</th><th>Found</th><th>Status</th><th>Role</th><th>Actions</th></tr>\n')
    f.write('                    </thead>\n')
    f.write('                    <tbody>\n')
    f.write('                        {% for user in users %}\n')
    f.write('                        <tr>\n')
    f.write('                            <td><a href="{% url "user_detail" user.id %}">{{ user.username }}</a></td>\n')
    f.write('                            <td>{{ user.email|default:"-" }}</td>\n')
    f.write('                            <td>{{ user.lost_count }}</td>\n')
    f.write('                            <td>{{ user.found_count }}</td>\n')
    f.write('                            <td>{% if user.is_active %}<span class="badge bg-success">Active</span>{% else %}<span class="badge bg-danger">Inactive</span>{% endif %}</td>\n')
    f.write('                            <td>{% if user.is_staff %}<span class="badge bg-primary">Staff</span>{% else %}<span class="badge bg-secondary">User</span>{% endif %}</td>\n')
    f.write('                            <td>\n')
    f.write('                                {% if user != request.user %}\n')
    f.write('                                <a href="{% url "toggle_user_status" user.id %}" class="btn btn-sm btn-warning">{% if user.is_active %}Deactivate{% else %}Activate{% endif %}</a>\n')
    f.write('                                <a href="{% url "delete_user" user.id %}" class="btn btn-sm btn-danger" onclick="return confirm(\'Delete this user?\')">Delete</a>\n')
    f.write('                                {% else %}<span class="text-muted">(You)</span>{% endif %}\n')
    f.write('                            </td>\n')
    f.write('                        </tr>\n')
    f.write('                        {% endfor %}\n')
    f.write('                    </tbody>\n')
    f.write('                </table>\n')
    f.write('            </div>\n')
    f.write('        </div>\n')
    f.write('    </div>\n')
    f.write('</div>\n')
    f.write('{% endblock %}\n')
print("✅ user_management.html fixed")

# 2. Fix user_detail.html
print("\n📝 Fixing user_detail.html...")
with open('templates/user_detail.html', 'w') as f:
    f.write('{% extends "base.html" %}\n')
    f.write('\n')
    f.write('{% block content %}\n')
    f.write('<div class="container mt-4">\n')
    f.write('    <div class="card shadow">\n')
    f.write('        <div class="card-header bg-primary text-white">\n')
    f.write('            <h3><i class="bi bi-person-circle"></i> {{ user_detail.username }}</h3>\n')
    f.write('        </div>\n')
    f.write('        <div class="card-body">\n')
    f.write('            <div class="row">\n')
    f.write('                <div class="col-md-6">\n')
    f.write('                    <h5>Account Information</h5>\n')
    f.write('                    <p><strong>Email:</strong> {{ user_detail.email|default:"-" }}<br>\n')
    f.write('                    <strong>Joined:</strong> {{ user_detail.date_joined|date:"M d, Y" }}<br>\n')
    f.write('                    <strong>Status:</strong> {% if user_detail.is_active %}Active{% else %}Inactive{% endif %}<br>\n')
    f.write('                    <strong>Role:</strong> {% if user_detail.is_staff %}Staff{% else %}User{% endif %}</p>\n')
    f.write('                </div>\n')
    f.write('                <div class="col-md-6">\n')
    f.write('                    <h5>Statistics</h5>\n')
    f.write('                    <p><strong>Lost Items:</strong> {{ lost_count }}<br>\n')
    f.write('                    <strong>Found Items:</strong> {{ found_count }}<br>\n')
    f.write('                    <strong>Notifications:</strong> {{ unread_notifications }}</p>\n')
    f.write('                </div>\n')
    f.write('            </div>\n')
    f.write('            <a href="{% url "user_management" %}" class="btn btn-secondary"><i class="bi bi-arrow-left"></i> Back to Users</a>\n')
    f.write('        </div>\n')
    f.write('    </div>\n')
    f.write('</div>\n')
    f.write('{% endblock %}\n')
print("✅ user_detail.html fixed")

# 3. Fix views.py - Remove duplicates
print("\n📝 Fixing views.py (removing duplicates)...")
with open('system/views.py', 'r') as f:
    content = f.read()

# Find where the duplicate starts and remove it
# Keep only the first occurrence of user management functions
lines = content.split('\n')
new_lines = []
seen_functions = set()
skip_until = None

for line in lines:
    # Check if this is a duplicate function definition
    if 'def user_management(request):' in line:
        if 'user_management' in seen_functions:
            skip_until = 'def '
            continue
        seen_functions.add('user_management')
    elif 'def toggle_user_status' in line:
        if 'toggle_user_status' in seen_functions:
            skip_until = 'def '
            continue
        seen_functions.add('toggle_user_status')
    elif 'def make_staff' in line:
        if 'make_staff' in seen_functions:
            skip_until = 'def '
            continue
        seen_functions.add('make_staff')
    elif 'def delete_user' in line:
        if 'delete_user' in seen_functions:
            skip_until = 'def '
            continue
        seen_functions.add('delete_user')
    elif 'def user_detail' in line:
        if 'user_detail' in seen_functions:
            skip_until = 'def '
            continue
        seen_functions.add('user_detail')
    elif 'def unread_notification_count' in line:
        if 'unread_notification_count' in seen_functions:
            skip_until = 'def '
            continue
        seen_functions.add('unread_notification_count')
    
    # Skip lines while in duplicate block
    if skip_until and line.strip().startswith(skip_until):
        skip_until = None
        continue
    if skip_until:
        continue
    
    new_lines.append(line)

with open('system/views.py', 'w') as f:
    f.write('\n'.join(new_lines))
print("✅ views.py cleaned (duplicates removed)")

# 4. Add missing notification bell to base.html
print("\n📝 Adding notification bell to base.html...")
with open('templates/base.html', 'r') as f:
    content = f.read()

if 'bi-bell' not in content:
    # Add notification bell before logout
    content = content.replace(
        '{% if user.is_authenticated %}',
        '{% if user.is_authenticated %}\n                <li class="nav-item">\n                    <a class="nav-link" href="{% url \'notifications\' %}">\n                        <i class="bi bi-bell-fill"></i>\n                    </a>\n                </li>'
    )
    with open('templates/base.html', 'w') as f:
        f.write(content)
    print("✅ Notification bell added")
else:
    print("⏩ Notification bell already exists")

print("\n" + "=" * 60)
print("✅ ALL FIXES COMPLETE!")
print("=" * 60)
print("\nNow run:")
print("git add .")
print("git commit -m 'Final fix - templates and duplicate removal'")
print("git push origin master")
print("\nThen redeploy on Render!")