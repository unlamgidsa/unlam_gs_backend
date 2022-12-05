from django.contrib import admin

from .models.CommandType import CommandType
from .models.CommandTypeParameter import CommandTypeParameter  
from .models.CommandTypeParameter import CommandTypeParameter 
# Register your models here.




class CommandTypeParametersInline(admin.TabularInline):
    model = CommandTypeParameter



class CommandTypeAdmin(admin.ModelAdmin):
    empty_value_display = ''
    fields = ('code', 'description', 'active', 'transactional', 'satellite', 'satelliteStates', 'maxRetry', 'commandCode', 'timeout', 'notes')
    list_display = ('code', 'description', 'transactional', 'satellite', 'timeout', 'notes')
    #list_filter = (NameFilter,)
    search_fields = ['code']
    inlines = [
        CommandTypeParametersInline,
    ]

admin.site.register(CommandType, CommandTypeAdmin)
