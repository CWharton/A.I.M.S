# Generated by Django 2.0.7 on 2018-09-05 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20170504_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='assetchangelog',
            options={'ordering': ('created',)},
        ),
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='subtype',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'ordering': ('name',)},
        ),
    ]
