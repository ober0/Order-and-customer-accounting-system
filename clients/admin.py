from django.contrib import admin
from .models import Clients


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'mobile_phone',)
    search_fields = ('id', 'first_name', 'last_name', 'email', 'mobile_phone')
    ordering = ('id',)
