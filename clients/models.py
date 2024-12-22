from django.db import models

class Clients(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    mobile_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Номер телефона')
    email = models.EmailField(max_length=100, null=False, blank=False, verbose_name='Эл. почта')
    added_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name} {self.middle_name} '
        return f'{self.last_name} {self.first_name}'