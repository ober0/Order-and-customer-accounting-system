from django.contrib import admin
from .models import Clients


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile_phone',)
    search_fields = ('first_name', 'last_name', 'email', 'mobile_phone')
    ordering = ('first_name',)
