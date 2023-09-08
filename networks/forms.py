from django import forms

from assets.models import Asset
from networks.models import Network, AssetNetwork


class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ['name', 'ipv4_address', 'ipv4_netmask', 'assigned_on', 'comment']

    assigned_on = forms.ModelChoiceField(queryset=Asset.objects.all(), to_field_name='name')
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))


class AssetNetworkForm(forms.ModelForm):
    class Meta:
        model = AssetNetwork
        widgets = {'asset': forms.HiddenInput()}
        fields = ['asset', 'name', 'ipv4_address', 'mac_address', 'network_type', 'network']

    ipv4_address = forms.GenericIPAddressField(label='IPv4 Address', required=False, protocol='IPv4')
    mac_address = forms.CharField(label='MAC Address', required=False)

