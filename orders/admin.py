from django.contrib import admin
from .models import Orders


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'product', 'quantity', 'total_price', 'status', 'created_at')  # Поля для отображения
    list_filter = ('status', 'client', 'created_at')  # Фильтры по полям
    search_fields = ('product', 'client__name')  # Поля для поиска
    ordering = ('-created_at',)