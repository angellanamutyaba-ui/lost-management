from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        groups = ['Moderators', 'Viewers', 'Editors']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            self.stdout.write(f'{"Created" if created else "Already exists"} group: {group_name}')
        
        # Add admin to Moderators
        try:
            admin = User.objects.get(username='admin')
            moderator = Group.objects.get(name='Moderators')
            admin.groups.add(moderator)
            self.stdout.write('Added admin to Moderators group')
        except User.DoesNotExist:
            self.stdout.write('Admin user not found')
        
        self.stdout.write(self.style.SUCCESS('✅ Groups created successfully!'))