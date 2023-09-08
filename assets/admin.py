from django.contrib import admin

# Register your models here.
from assets.models import Asset, Type, SubType, Manufacturer, Status

admin.site.register(Asset)
admin.site.register(Status)
admin.site.register(Manufacturer)
admin.site.register(Type)
admin.site.register(SubType)
