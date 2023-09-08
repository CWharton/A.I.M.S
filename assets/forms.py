from django import forms

from assets.models import Asset, Status, Manufacturer, Type, SubType, Note


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['type']

    type = forms.ModelChoiceField(queryset=Type.objects.all(), to_field_name='name')


class AssetCreateForm(forms.ModelForm):
    def __init__(self, list_type, *args, **kwargs):
        super(AssetCreateForm, self).__init__(*args, **kwargs)
        self.fields["sub_type"].label = list_type + ' Type'
        self.fields["sub_type"].queryset = SubType.objects.filter(type__name__iexact=list_type)

    class Meta:
        model = Asset
        widgets = {'type': forms.HiddenInput()}
        fields = ['name', 'type', 'sub_type', 'manufacturer', 'model', 'status', 'serial', 'other_serial',
                  'inventory_number', 'station_id', 'location', 'purchased', 'purchased_price']

    name = forms.CharField(required=True)
    other_serial = forms.CharField(required=False, max_length=255)
    inventory_number = forms.CharField(label='Inventory Number', required=False, max_length=255)
    station_id = forms.CharField(label='Station ID', required=False, max_length=255)
    location = forms.CharField(required=False, max_length=255)
    purchased = forms.DateField(label='Purchase Date', required=False)
    purchased_price = forms.DecimalField(label='Purchase Amount', required=False, decimal_places=2)
    sub_type = forms.ModelChoiceField(label='Sub-Type', queryset=SubType.objects.all(), required=False)

    def clean_serial(self):
        serial = self.cleaned_data['serial']
        manufacturer = self.cleaned_data['manufacturer']
        if Asset.objects.filter(serial=serial, manufacturer=manufacturer).exclude(pk=self.instance.pk).count() > 0:
            raise forms.ValidationError("Serial number is already in use")
        return serial


class AssetSafeForm(forms.ModelForm):
    def __init__(self, list_type, *args, **kwargs):
        super(AssetSafeForm, self).__init__(*args, **kwargs)
        self.fields["sub_type"].label = list_type + ' Type'
        self.fields["sub_type"].queryset = SubType.objects.filter(type__name__iexact=list_type)

    class Meta:
        model = Asset
        widgets = {'type': forms.HiddenInput()}
        fields = ['type', 'sub_type', 'manufacturer', 'model', 'serial', 'other_serial', 'inventory_number',
                  'purchased', 'purchased_price', 'omit_audit']

    other_serial = forms.CharField(required=False, max_length=255)
    inventory_number = forms.CharField(label='Inventory Number', required=False, max_length=255)
    purchased = forms.DateField(label='Purchase Date', required=False)
    purchased_price = forms.DecimalField(label='Purchase Amount', required=False, decimal_places=2)
    sub_type = forms.ModelChoiceField(label='Sub-Type', queryset=SubType.objects.all(), required=False)
    omit_audit = forms.BooleanField(required=False, label='Omit from audit report')

    def clean_serial(self):
        serial = self.cleaned_data['serial']
        manufacturer = self.cleaned_data['manufacturer']
        if Asset.objects.filter(serial=serial, manufacturer=manufacturer).exclude(pk=self.instance.pk).count() > 0:
            raise forms.ValidationError("Serial number is already in use")
        return serial


class AssetChangeForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'status', 'station_id', 'location', 'comment']

    name = forms.CharField(required=True)
    comment = forms.CharField(label='Internal comment', required=False, widget=forms.Textarea(attrs={'rows': 3}))
    station_id = forms.CharField(label='Station ID', required=False, max_length=255)
    location = forms.CharField(required=False, max_length=255)


class AssetCheckInForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'status', 'location']

    location = forms.CharField(required=False, max_length=255)


class AssetDeleteForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['decommissioned_reason']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'fa_class']

    fa_class = forms.CharField(
        required=False,
        max_length=50,
        label='Font Awesome Class',
        help_text='Use "<a href="http://fontawesome.io/icons/" target="_new">Font Awesome</a>" icons to assign a icon class.)'
    )


class SubTypeForm(forms.ModelForm):
    class Meta:
        model = SubType
        fields = ['type', 'name', 'fa_class']

    fa_class = forms.CharField(
        required=False,
        max_length=50,
        label='Font Awesome Class',
        help_text='Use "<a href="http://fontawesome.io/icons/" target="_new">Font Awesome</a>" icons to assign a icon class.)'
    )


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        widgets = {'asset': forms.HiddenInput()}
        fields = ['asset', 'comment']

    comment = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={'rows': 3}))
