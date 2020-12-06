from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from quest.models import Action, Record, Quest


# Register your models here.
@admin.register(Action)
class ActionAdmin(ImportExportModelAdmin):#admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'xp', )
    list_display_links = ('id', 'name',)
    list_filter = ('category',)


@admin.register(Quest)
class QuestAdmin(ImportExportModelAdmin):#admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'xp',)
    list_display_links = ('id', 'name',)
    list_filter = ('category',)


@admin.register(Record)
class RecordAdmin(ImportExportModelAdmin):#admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'memo', 'repeat', 'xp', 'date', 'time',  'checked',)
    list_display_links = ('id', 'action',)
    list_filter = ('user', 'action', 'date', )
    list_editable = ['checked']
    