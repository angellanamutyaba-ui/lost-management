from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Add items
    path('add-lost/', views.add_lost, name='add_lost'),
    path('add-found/', views.add_found, name='add_found'),
    
    # Claim items
    path('claim-lost/<int:id>/', views.claim_lost, name='claim_lost'),
    path('claim-found/<int:id>/', views.claim_found, name='claim_found'),
    
    # Admin actions - Lost items
    path('approve-lost/<int:id>/', views.approve_lost, name='approve_lost'),
    path('reject-lost/<int:id>/', views.reject_lost, name='reject_lost'),
    path('delete-lost/<int:id>/', views.delete_lost, name='delete_lost'),
    
    # Admin actions - Found items
    path('approve-found/<int:id>/', views.approve_found, name='approve_found'),
    path('reject-found/<int:id>/', views.reject_found, name='reject_found'),
    path('delete-found/<int:id>/', views.delete_found, name='delete_found'),
    
    # Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark/<int:id>/', views.mark_notification_read, name='mark_notification_read'),
    path('alert-preferences/', views.alert_preferences, name='alert_preferences'),
]