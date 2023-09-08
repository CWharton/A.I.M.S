from django.contrib.auth.models import User
from django.core import management
from django.core.management import BaseCommand

from assets.models import Status, Type, SubType


class Command(BaseCommand):
    help = 'Initializes database for usage'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(pk=1)  # TODO: Change to first created account
        except User.DoesNotExist:
            self.stdout.write(self.style.NOTICE('Creating Super User Account...'))
            management.call_command('createsuperuser')
            user = User.objects.get(pk=1)

        Status.objects.bulk_create([
            Status(name='In Use', created_by=user, modified_by=user),
            Status(name='Shelved', created_by=user, modified_by=user),
            Status(name='Defective', created_by=user, modified_by=user),
            Status(name='Needs Repair', created_by=user, modified_by=user)
        ])

        Type.objects.bulk_create([
            Type(name='Computer', created_by=user, modified_by=user),
            Type(name='Monitor', created_by=user, modified_by=user),
            Type(name='Network', created_by=user, modified_by=user),
            Type(name='Printer', created_by=user, modified_by=user),
            Type(name='Phone', created_by=user, modified_by=user)
        ])

        computer = Type.objects.get(name='Computer')
        network = Type.objects.get(name='Network')
        printer = Type.objects.get(name='Printer')
        phone = Type.objects.get(name='Phone')

        SubType.objects.bulk_create([
            SubType(name='Desktop', type=computer,  created_by=user, modified_by=user),
            SubType(name='Laptop', type=computer, created_by=user, modified_by=user),
            SubType(name='Tablet', type=computer, created_by=user, modified_by=user),
            SubType(name='Server', type=computer, created_by=user, modified_by=user),

            SubType(name='Router', type=network, created_by=user, modified_by=user),
            SubType(name='Switch', type=network, created_by=user, modified_by=user),

            SubType(name='Laser', type=printer, created_by=user, modified_by=user),
            SubType(name='InkJet', type=printer, created_by=user, modified_by=user),

            SubType(name='Mobile', type=phone, created_by=user, modified_by=user),
            SubType(name='Desk', type=phone, created_by=user, modified_by=user),
        ])

        self.stdout.write(self.style.SUCCESS('Successfully initialized database'))
