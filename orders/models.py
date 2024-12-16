from django.db import models

from clients.models import Clients


class Orders(models.Model):
    # Поля заказа
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент")  # Клиент
    product = models.CharField(max_length=255, verbose_name="Товар")  # Название товара
    quantity = models.PositiveIntegerField(verbose_name="Количество")  # Количество товара
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")  # Цена за единицу товара
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Итоговая цена")  # Итоговая цена
    description = models.TextField(blank=True, verbose_name="Описание заказа")  # Описание заказа
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'В ожидании'), ('Completed', 'Завершено'), ('Cancelled', 'Отменено')],
        default='Pending',
        verbose_name="Статус заказа"
    )  # Статус заказа
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")  # Дата создания

    def save(self, *args, **kwargs):
        # Автоматический расчет итоговой цены
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at', 'total_price']

    def __str__(self):
        return f'Заказ #{self.id}'
