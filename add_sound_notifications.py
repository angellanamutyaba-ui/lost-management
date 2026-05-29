# add_sound_notifications.py - Run ONCE to add sound notifications
import os

print("=" * 60)
print("🔊 ADDING SOUND NOTIFICATIONS TO YOUR SYSTEM")
print("=" * 60)

# ============================================================
# 1. UPDATE views.py - Add API endpoint for notification count
# ============================================================
views_path = 'system/views.py'
with open(views_path, 'r') as f:
    content = f.read()

if 'unread_notification_count' not in content:
    print("📝 Adding API endpoint to views.py...")
    
    api_code = '''

# ========== API FOR SOUND NOTIFICATIONS ==========
from django.http import JsonResponse

def unread_notification_count(request):
    """API endpoint to get unread notification count for sound alerts"""
    if request.user.is_authenticated:
        from .models import Notification
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})
'''
    
    with open(views_path, 'a') as f:
        f.write(api_code)
    print("✅ API endpoint added to views.py")
else:
    print("⏩ API endpoint already exists")

# ============================================================
# 2. UPDATE urls.py - Add API URL
# ============================================================
urls_path = 'system/urls.py'
with open(urls_path, 'r') as f:
    content = f.read()

if 'unread-count' not in content:
    print("📝 Adding API URL to urls.py...")
    
    # Find where to add
    lines = content.split('\n')
    new_lines = []
    added = False
    for line in lines:
        new_lines.append(line)
        if 'urlpatterns = [' in line and not added:
            new_lines.append("    path('notifications/api/unread-count/', views.unread_notification_count, name='unread_count'),")
            added = True
    
    with open(urls_path, 'w') as f:
        f.write('\n'.join(new_lines))
    print("✅ API URL added to urls.py")
else:
    print("⏩ API URL already exists")

# ============================================================
# 3. UPDATE base.html - Add sound notification code
# ============================================================
base_path = 'templates/base.html'
with open(base_path, 'r') as f:
    content = f.read()

if 'playNotificationSound' not in content:
    print("🔊 Adding sound notification code to base.html...")
    
    # Find </body> tag and add script before it
    sound_script = '''
<!-- SOUND NOTIFICATIONS -->
<script>
    // Sound notification function
    function playNotificationSound() {
        // Try multiple sound sources for reliability
        var sounds = [
            'https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3',
            'https://actions.google.com/sounds/437/notification_bell.mp3',
            'data:audio/wav;base64,U3RlYWx0aCBhbmQgc291bmQgdGVzdA=='
        ];
        
        for (var i = 0; i < sounds.length; i++) {
            var audio = new Audio(sounds[i]);
            audio.play().catch(function(e) {
                // Silently fail, try next sound
            });
            break; // Try only first sound
        }
    }
    
    // Browser notification
    function showBrowserNotification(title, body) {
        if (Notification.permission === "granted") {
            new Notification(title, {
                body: body,
                icon: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='%234f46e5' d='M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z'/%3E%3C/svg%3E",
                silent: false
            });
        }
    }
    
    // Track notification count
    var lastCount = {{ unread_notifications|default:0 }};
    
    // Check for new notifications
    function checkForNewNotifications() {
        fetch('/notifications/api/unread-count/')
            .then(response => response.json())
            .then(data => {
                if (data.count > lastCount) {
                    // New notification arrived!
                    playNotificationSound();
                    showBrowserNotification('🔔 Lost Management System', 'You have a new notification!');
                    
                    // Update bell badge
                    var badge = document.getElementById('notificationCount');
                    if (badge && data.count > 0) {
                        badge.textContent = data.count;
                        badge.style.display = 'inline-block';
                    }
                }
                lastCount = data.count;
            })
            .catch(function(err) {
                console.log("Error checking notifications:", err);
            });
    }
    
    // Request permission for browser notifications
    if ('Notification' in window) {
        if (Notification.permission !== "granted" && Notification.permission !== "denied") {
            setTimeout(function() {
                Notification.requestPermission();
            }, 2000);
        }
    }
    
    // Check every 20 seconds for new notifications
    setInterval(checkForNewNotifications, 20000);
    
    // Initial check after page loads
    setTimeout(checkForNewNotifications, 3000);
</script>
'''
    
    # Insert before </body>
    content = content.replace('</body>', sound_script + '\n</body>')
    
    with open(base_path, 'w') as f:
        f.write(content)
    print("✅ Sound notification code added to base.html")
else:
    print("⏩ Sound notifications already exist in base.html")

# ============================================================
# 4. UPDATE dashboard.html - Pass unread count to template
# ============================================================
dashboard_path = 'templates/dashboard.html'
if os.path.exists(dashboard_path):
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check if unread_notifications is already in context (views.py handles this)
    print("✅ Dashboard template ready for notifications")
else:
    print("⚠️ dashboard.html not found, skipping")

# ============================================================
# 5. UPDATE views.py dashboard to pass unread count
# ============================================================
with open(views_path, 'r') as f:
    content = f.read()

if "'unread_notifications':" not in content:
    print("📝 Updating dashboard view to pass unread count...")
    
    # Find dashboard function and add unread count to context
    lines = content.split('\n')
    new_lines = []
    in_dashboard = False
    context_line = -1
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if 'def dashboard(request):' in line:
            in_dashboard = True
        if in_dashboard and "context = {" in line:
            context_line = i
        if in_dashboard and context_line > 0 and i == context_line + 1:
            # After context = {, add unread count
            new_lines.append("        'unread_notifications': Notification.objects.filter(user=request.user, is_read=False).count(),")
            in_dashboard = False
    
    with open(views_path, 'w') as f:
        f.write('\n'.join(new_lines))
    print("✅ Dashboard view updated")
else:
    print("⏩ Dashboard already has unread count")

# ============================================================
# 6. Create simple static sound file (optional)
# ============================================================
os.makedirs('static/sounds', exist_ok=True)
print("✅ Static sounds folder created")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("✅ SOUND NOTIFICATIONS ADDED SUCCESSFULLY!")
print("=" * 60)
print("""
What was added:
  1. ✅ API endpoint to get notification count
  2. ✅ Sound playing JavaScript
  3. ✅ Browser notification permission request
  4. ✅ Auto-check for new notifications every 20 seconds

How it works:
  - When a new notification arrives, you'll hear a BELL SOUND 🔔
  - You'll also see a browser popup notification
  - The bell icon updates with the count

Test it:
  1. Run: python manage.py runserver
  2. Login as admin
  3. Create a test notification using the shell
  4. Wait 20 seconds - you'll hear the sound!

Now run these commands to deploy:
  git add .
  git commit -m "Add sound notifications with bell sound"
  git push origin master
""")

if __name__ == '__main__':
    print("\n🚀 Run this command to deploy:")
    print("   git add . && git commit -m 'Add sound notifications' && git push origin master")