from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import ShopProfile

class Command(BaseCommand):
    help = 'Create a default superuser for admin access'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Default superuser already exists'))
            return

        # Create superuser
        user = User.objects.create_superuser(
            username='admin',
            email='admin@pravinenterprises.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )

        # Create shop profile
        ShopProfile.objects.create(
            user=user,
            shop_name='Pravin Enterprises Admin',
            gst_number='22AAAAA0000A1Z5',  # Sample GST
            email='admin@pravinenterprises.com',
            phone_number='+919876543210',
            shop_address='Admin Office',
            city='Mumbai',
            state='Maharashtra',
            postal_code='400001'
        )

        self.stdout.write(self.style.SUCCESS('Default superuser created successfully'))
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
        self.stdout.write('Email: admin@pravinenterprises.com')