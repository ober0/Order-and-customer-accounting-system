from django.db import models

class Report(models.Model):
    PERIOD_CHOICES = [
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ('year', 'Год'),
    ]

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, verbose_name="Период")

    new_orders_count = models.PositiveIntegerField(default=0, verbose_name="Кол-во новых заказов")
    new_clients_count = models.PositiveIntegerField(default=0, verbose_name="Кол-во новых клиентов")
    total_orders_sum = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Сумма новых заказов")
    avg_order_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Средняя сумма заказов")
    completed_orders_count = models.PositiveIntegerField(default=0, verbose_name="Кол-во выполненных заказов")

    def __str__(self):
        return f"Отчет за {self.get_period_display()} - {self.date_created.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
