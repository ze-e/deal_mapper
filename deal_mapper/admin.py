from django.contrib import admin

# Register your models here.
from .models import Current_Property
from .models import Archived_Property
from .models import DB_Update

admin.site.register(Current_Property)
admin.site.register(Archived_Property)
admin.site.register(DB_Update)
