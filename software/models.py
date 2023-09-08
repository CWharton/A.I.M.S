from django.conf import settings
from django.db import models

from assets.models import Asset


class Software(models.Model):
    name = models.CharField(max_length=255)
    comment = models.TextField()
    available_licenses = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class AssetLicense(models.Model):
    asset = models.ForeignKey(Asset, null=False, related_name='licenses', on_delete=models.CASCADE)
    software = models.ForeignKey(Software, null=False, related_name='+', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    serial_number = models.TextField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
