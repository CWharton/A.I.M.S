from django.contrib.auth.models import User
from django.core import management
from django.core.management import BaseCommand

from assets.models import Status, Type, SubType, Asset, Manufacturer
from networks.models import Network


class Command(BaseCommand):
    help = 'Initializes database for usage'

    def handle(self, *args, **options):
        management.call_command('migrate')
        user = User(username='dev', email='dev@automax.com', first_name='Dev', last_name='User', is_active=True, is_superuser=True)
        user.set_password('dev')
        user.save()

        Status.objects.bulk_create([
            Status(name='In Use', created_by=user, modified_by=user),
            Status(name='Shelved', created_by=user, modified_by=user),
            Status(name='Defective', created_by=user, modified_by=user),
            Status(name='Needs Repair', created_by=user, modified_by=user)
        ])

        status_inuse = Status.objects.get(name='In Use')
        status_shelved = Status.objects.get(name='Shelved')

        Type.objects.bulk_create([
            Type(name='Computer', fa_class='fa-desktop', created_by=user, modified_by=user),
            Type(name='Monitor', fa_class='fa-monitor', created_by=user, modified_by=user),
            Type(name='Network', fa_class='fa-desktop', created_by=user, modified_by=user),
            Type(name='Printer', fa_class='fa-print', created_by=user, modified_by=user),
            Type(name='Phone', fa_class='fa-phone', created_by=user, modified_by=user)
        ])

        type_computer = Type.objects.get(name='Computer')
        type_network = Type.objects.get(name='Network')
        type_printer = Type.objects.get(name='Printer')
        type_phone = Type.objects.get(name='Phone')

        SubType.objects.bulk_create([
            SubType(name='Desktop', fa_class='fa-desktop', type=type_computer, created_by=user, modified_by=user),
            SubType(name='Laptop', fa_class='fa-laptop', type=type_computer, created_by=user, modified_by=user),
            SubType(name='Tablet', fa_class='fa-tablet', type=type_computer, created_by=user, modified_by=user),
            SubType(name='Server', fa_class='fa-server', type=type_computer, created_by=user, modified_by=user),

            SubType(name='Router', fa_class='fa-desktop', type=type_network, created_by=user, modified_by=user),
            SubType(name='Switch', fa_class='fa-desktop', type=type_network, created_by=user, modified_by=user),

            SubType(name='Laser', fa_class='fa-print', type=type_printer, created_by=user, modified_by=user),
            SubType(name='InkJet', fa_class='fa-print', type=type_printer, created_by=user, modified_by=user),

            SubType(name='Mobile', fa_class='fa-mobile', type=type_phone, created_by=user, modified_by=user),
            SubType(name='Desk', fa_class='fa-phone', type=type_phone, created_by=user, modified_by=user),
        ])

        subtype_desktop = SubType.objects.get(name='Desktop')
        subtype_laptop = SubType.objects.get(name='Laptop')
        subtype_laser = SubType.objects.get(name='Laser')
        subtype_desk = SubType.objects.get(name='Desk')
        subtype_router = SubType.objects.get(name='Router')

        Manufacturer.objects.bulk_create([
            Manufacturer(name='Dell', created_by=user, modified_by=user),
            Manufacturer(name='Hewlett-Packard', created_by=user, modified_by=user),
            Manufacturer(name='Panasonic', created_by=user, modified_by=user),
            Manufacturer(name='pfSense', created_by=user, modified_by=user),
        ])

        manufacturer_de11 = Manufacturer.objects.get(name='Dell')
        manufacturer_hp = Manufacturer.objects.get(name='Hewlett-Packard')
        manufacturer_panasonic = Manufacturer.objects.get(name='Panasonic')
        manufacturer_pfsense = Manufacturer.objects.get(name='pfSense')

        # Computers
        Asset.objects.bulk_create([
            Asset(name='33D0XR1', serial='6733624285', other_serial='250', type=type_computer, sub_type=subtype_desktop,
                  manufacturer=manufacturer_de11, model='Optiplex 390', location='I.T. Office', status=status_shelved, created_by=user,
                  modified_by=user),
            Asset(name='B0PWJH2', serial='23988114326', other_serial='', type=type_computer, sub_type=subtype_desktop, manufacturer=manufacturer_de11,
                  model='Optiplex 5040', location='Controller Office', status=status_inuse, created_by=user, modified_by=user),
        ])

        # Printers
        Asset.objects.bulk_create([
            Asset(name='hp_m601', serial='123456789', other_serial='24', type=type_printer, sub_type=subtype_laser, manufacturer=manufacturer_hp,
                  model='M601', location='I.T. Office', status=status_inuse, created_by=user, modified_by=user)
        ])

        # Phone
        Asset.objects.bulk_create([
            Asset(name='panac_analog_001', serial='0ACID047564', other_serial='', type=type_phone, sub_type=subtype_desk, status=status_inuse,
                  manufacturer=manufacturer_panasonic, model='KX-T7433-B', location='I.T. Office', created_by=user, modified_by=user)
        ])

        # Asset Network
        Asset.objects.bulk_create([
            Asset(name='server-gw', serial='0ACID047564', other_serial='', type=type_network, sub_type=subtype_router, status=status_inuse,
                  manufacturer=manufacturer_pfsense, model='KX-T7433-B', location='Ford Network Closet', created_by=user, modified_by=user)
        ])

        # Network
        asset_pfsense = Asset.objects.get(name='server-gw')
        Network.objects.bulk_create([
            Network(name='Server', ipv4_address='10.18.1.1', ipv4_netmask='255.255.255.0', assigned_on=asset_pfsense, created_by=user,
                    modified_by=user)
        ])

        self.stdout.write(self.style.SUCCESS('Successfully initialized database'))
