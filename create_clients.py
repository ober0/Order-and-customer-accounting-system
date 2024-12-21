import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrderAndCustomerAccountingSystem.settings')
django.setup()

from clients.models import Clients

fake = Faker('ru_RU')

def populate_clients():
    for _ in range(1000):
        is_male = random.choice([True, False])

        if is_male:
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
            middle_name = fake.middle_name_male()
        else:
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()
            middle_name = fake.middle_name_female()

        Clients.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=fake.email(),
            mobile_phone=fake.phone_number(),
            middle_name=middle_name,
        )

    print("1000 клиентов успешно добавлены.")

if __name__ == '__main__':
    populate_clients()
