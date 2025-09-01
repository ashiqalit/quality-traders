from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            username = config('DJANGO_SUPERUSER_USERNAME')
            email = config('DJANGO_SUPERUSER_EMAIL')
            password = config('DJANGO_SUPERUSER_PASSWORD')

            if not all([username, email, password]):
                self.stdout.write(self.style.ERROR('Superuser environment variables not set. Skipping... '))
                return
            self.stdout.write('Creating superuser...')
            try:
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
        else:
            self.stdout.write('Superuser already exists. Skipping... ')