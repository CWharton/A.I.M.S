from django.conf import settings
from django.db import models

from assets.models import Asset


class Network(models.Model):
    name = models.CharField(max_length=255)
    ipv4_address = models.GenericIPAddressField(protocol='IPv4')
    ipv4_netmask = models.GenericIPAddressField(protocol='IPv4')
    assigned_on = models.ForeignKey(Asset, null=False, related_name='+', on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class AssetNetwork(models.Model):
    NETWORK_TYPE = (
        ('Wireless', 'Wireless'),
        ('Ethernet', 'Ethernet'),
        ('Alias', 'Alias'),
        ('Fiber', 'Fiber'),
    )
    name = models.CharField(max_length=255)
    ipv4_address = models.GenericIPAddressField(null=True, protocol='IPv4')
    mac_address = models.CharField(null=True, max_length=120)
    network_type = models.CharField(null=True, max_length=120, choices=NETWORK_TYPE)
    network = models.ForeignKey(Network, null=False, related_name='+', on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, null=False, related_name='networks', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
