from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ClientDB, Dashboard, Chart

admin.site.register(Dashboard)
admin.site.register(Chart)
admin.site.register(ClientDB)

