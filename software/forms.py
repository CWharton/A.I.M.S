from django import forms

from software.models import Software, AssetLicense


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ['name', 'available_licenses', 'comment']

    name = forms.CharField(required=True)
    comment = forms.CharField(label='Comments', required=False, widget=forms.Textarea(attrs={'rows': 3}))
    available_licenses = forms.IntegerField(label='Available licenses', required=False)


class AssetLicenseForm(forms.ModelForm):
    class Meta:
        model = AssetLicense
        widgets = {'asset': forms.HiddenInput()}
        fields = ['asset', 'software', 'serial_number', 'comment']

    serial_number = forms.CharField(label='Serial Number', required=False)
    comment = forms.CharField(label='Comments', required=False, widget=forms.Textarea(attrs={'rows': 3}))
