import datetime

from django.conf import settings
from django.db import models


# Current status of a asset
from django.utils.datetime_safe import date


class Status(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name',)


# Manufacturer of a asset
class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name',)


# Type of a asset (e.g. Computer, Printer, Network)
# TODO: Add validation to prevent spaces
class Type(models.Model):
    name = models.CharField(max_length=255)
    fa_class = models.CharField(null=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name',)


# Sub-Type of the type of asset (e.g. Desktop, Laser Printer, Switch)
class SubType(models.Model):
    type = models.ForeignKey(Type, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fa_class = models.CharField(null=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name',)


# Main Asset class
class Asset(models.Model):
    name = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)
    other_serial = models.CharField(max_length=255)
    inventory_number = models.CharField(max_length=255, null=True)
    station_id = models.CharField(max_length=255, null=True)
    status = models.ForeignKey(Status, null=False, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, null=False, on_delete=models.CASCADE)
    sub_type = models.ForeignKey(SubType, null=True, blank=False, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, null=False, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    purchased = models.DateField(null=True, blank=False)
    purchased_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=False)
    omit_audit = models.BooleanField(null=True)
    comment = models.TextField()
    decommissioned = models.DateField(null=True, blank=False)
    decommissioned_reason = models.TextField(null=True)
    decommissioned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    @property
    def ip_addresses(self):
        networks = self.networks.all()
        return ', '.join(str(e.ipv4_address) for e in networks)

    @property
    def equipment(self):
        return self.manufacturer.name + ' ' + str(self.model)

    @property
    def last_checkin(self):
        item = self.check_in.latest('created').created.date()
        return item

    @property
    def last_checkin_status(self):
        item = self.check_in.latest('created').created.date()
        set_time = date.today() - datetime.timedelta(days=90)
        return set_time < item

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name',)


class Note(models.Model):
    asset = models.ForeignKey(Asset, null=False, related_name='notes', on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comment)

    class Meta:
        ordering = ('-created',)


# Asset change log
class AssetChangeLog(models.Model):
    asset = models.ForeignKey(Asset, null=False, related_name='change_log', on_delete=models.CASCADE)
    log = models.TextField(null=False)
    ip = models.GenericIPAddressField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.log)

    class Meta:
        ordering = ('-created',)


# Asset Check-In
class AssetCheckIn(models.Model):
    asset = models.ForeignKey(Asset, null=False, related_name='check_in', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created)

    class Meta:
        ordering = ('-created',)


class PrintQueue(models.Model):
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.asset.name)

    class Meta:
        ordering = ('created',)
