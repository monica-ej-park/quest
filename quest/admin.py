from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from quest.models import Action


# Register your models here.
@admin.register(Action)
class ActionAdmin(ImportExportModelAdmin):#admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'xp', )
    list_display_links = ('id', 'name')
    list_filter = ('category',)
