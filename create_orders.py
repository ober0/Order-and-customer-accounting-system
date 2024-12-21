import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderAndCustomerAccountingSystem.settings')
django.setup()

from orders.models import Orders
from clients.models import Clients

fake = Faker('ru_RU')

def populate_orders():
    # Получаем список всех клиентов
    client_ids = list(Clients.objects.values_list('id', flat=True))

    if not client_ids:
        print("Нет доступных клиентов для создания заказов.")
        return

    clients = list(Clients.objects.all())
    orders_to_create = []

    for _ in range(1000):
        order = Orders(
            product=fake.word(),
            quantity=random.randint(1, 100),
            price=round(random.uniform(10.0, 5000.0), 2),
            client=random.choice(clients),
        )
        order.save()


    print("1000 заказов успешно добавлены.")

if __name__ == '__main__':
    populate_orders()



