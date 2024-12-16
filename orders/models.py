from django.db import models

from clients.models import Clients


class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент", null=False, blank=False)
    product = models.CharField(max_length=255, verbose_name="Товар", null=False, blank=False)
    quantity = models.PositiveIntegerField(verbose_name="Количество", null=False, blank=False, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу", null=False, blank=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Итоговая цена", null=False, blank=True)
    description = models.TextField(blank=True, verbose_name="Описание заказа", null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'В ожидании'), ('Completed', 'Завершено'), ('Cancelled', 'Отменено')],
        default='Pending',
        verbose_name="Статус заказа",
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at', 'total_price']

    def __str__(self):
        return f'Заказ #{self.id}'
