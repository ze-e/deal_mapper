from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Current_Property
from .models import Archived_Property
from .models import DB_Update

#admin.site.register(Current_Property)
admin.site.register(Archived_Property)
admin.site.register(DB_Update)


@admin.register(Current_Property)
class Current_PropertyAdmin(ImportExportModelAdmin):
    pass