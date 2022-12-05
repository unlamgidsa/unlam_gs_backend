from django.contrib import admin

# Register your models here.
from django.contrib import admin
from CODS.models import ReferenceSystem


class ReferenceSystemAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    list_filter = ['code', 'description']

admin.site.register(ReferenceSystem,ReferenceSystemAdmin)
