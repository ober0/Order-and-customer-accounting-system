
# Система учета заказов и клиентов

**Навигация**:
- [Мотивация](#мотивация)
- [Установка и запуск](#установка-и-запуск)
- [Превью веб-интерфейса](#превью-веб-интерфейса)
- [Мобильное приложение](#мобильное-приложение) 
- [API](#api)
  - [Получение JWT токена](#получение-jwt-токена)
  - [Обновление JWT токена](#обновление-jwt-токена)
  - [Работа с клиентами](#работа-с-клиентами)
  - [Работа с заказами](#работа-с-заказами)
  - [Работа с отчетами](#работа-с-отчетами)
- [Диаграммы](#диаграммы)
- [Технологический стек](#технологический-стек)
- [Участники проекта](#участники-проекта)


## Мотивация

Проект создан для автоматизации рутинных задач, связанных с управлением заказами и клиентами. Он помогает компаниям анализировать данные и улучшать взаимодействие с клиентами.

---

## Установка и запуск

1. **Скачивание репозитория**
   ```bash
   git clone https://github.com/your-repo/order-accounting-system.git
   cd order-accounting-system
   ```
2. **Установка зависимостей**
   - Создайте виртуальное окружение и активируйте его:
     ```bash
     python -m venv venv
     source venv/bin/activate # Linux/macOS
     venv\Scripts\activate   # Windows
     ```
   - Установите зависимости:
     ```bash
     pip install -r requirements.txt
     ```
3. **Настройка базы данных**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **При локальном тестировании измените `settings.py`**
    ```bash
    DEBUG = True  # Включить только для разработки, в продакшн-среде должно быть False
    ```
5. **Запуск сервера**
   ```bash
   python manage.py runserver
   ```

## Превью веб-интерфейса
   - Перейдите в браузере по адресу: [http://95.164.3.6:8001/](http://95.164.3.6:8001/).
   - Используйте логин `test` и пароль `test`.

---

## Мобильное приложение

Репозиторий мобильного приложения https://github.com/gurx0/mobile-CRM

---

## API

* Все API доступны по пути `/api/`.
* Добавьте access токен в заголовок запросов:
    ```
    Authorization: Bearer <ACCESS_TOKEN>
    ```

### Получение JWT токена

- **URL**: `/api/token/`
- **Метод**: POST
- **Описание**: Получение JWT токена для авторизации.
- **Пример запроса**:
  ```json
  {
      "username": "admin",
      "password": "admin"
  }
  ```
- **Пример ответа**:
  ```json
  {
      "access": "<ACCESS_TOKEN>",
      "refresh": "<REFRESH_TOKEN>"
  }
  ```

### Обновление JWT токена

- **URL**: `/api/token/refresh/`
- **Метод**: POST
- **Описание**: Обновление Access токена.
- **Пример запроса**:
  ```json
  {
      "refresh": "<REFRESH_TOKEN>"
  }
  ```
- **Пример ответа**:
  ```json
  {
      "access": "<NEW_ACCESS_TOKEN>"
  }
  ```

---

### Работа с клиентами

#### Добавление клиента

- **URL**: `/api/clients/add/`
- **Метод**: POST
- **Пример запроса**:
  ```json
  {
      "first_name": "Иван",  // Обязательно поле (Имя клиента)
      "last_name": "Иванов",  // Обязательно поле (Фамилия клиента)
      "middle_name": "Иванович",
      "mobile_phone": "+79001234567",
      "email": "ivanov@example.com"  // Обязательно поле (Email клиента)
  }
  ```
- **Пример ответа**:
  ```json
  {
      "success": true,
      "id": 102
  }
  ```

#### Получение одного клиента по ID

- **URL**: `/api/clients/get/<int:id>/`
- **Метод**: POST
- **Пример ответа**:
  ```json
  {
      "client": {
          "id": 1,
          "first_name": "Иван",
          "last_name": "Иванов",
          "middle_name": "Иванович",
          "mobile_phone": "+79001234567",
          "email": "ivanov@example.com"
      }
  }
  ```

#### Получение списка клиентов

- **URL**: `/api/clients/get/`
- **Метод**: POST
- **Пример запроса**:
  ```json
  {
      "start_id": 0,  // Количество уже загруженных клиентов
      "status": "active",  // Статус клиентов 
      "search": "Анатолий",  // Поиск по ФИО, почте, телефону
      "order_by": "-id"  // Сортировка по ID в порядке убывания
  }
  ```
- **Пример ответа**:
  ```json
  {
      "clients": [
          {
              "id": 1,
              "first_name": "Иван",
              "last_name": "Иванов",
              "middle_name": "Иванович",
              "mobile_phone": "+79001234567",
              "email": "ivanov@example.com"
          }
      ]
  }
  ```

#### Редактирование клиента

- **URL**: `/api/clients/edit/<int:id>/`
- **Метод**: POST
- **Пример запроса**:
  ```json
  {
      "first_name": "Петр",
      "last_name": "Петров"
  }
  ```
- **Пример ответа**:
  ```json
  {
      "success": true,
      "id": 101
  }
  ```

#### Удаление клиента

- **URL**: `/api/clients/delete/<int:id>/`
- **Метод**: DELETE
- **Пример ответа**:
  ```json
  {
      "success": true
  }
  ```

---

### Работа с заказами

#### Добавление заказа

- **URL**: `/api/orders/add/`
- **Метод**: POST
- **Пример запроса**:
  ```json
  {
      "client": 1,
      "product": "Ноутбук",
      "quantity": 2,
      "price": "1500.00",
      "description": "Заказ ноутбука"
  }
  ```
- **Пример ответа**:
  ```json
  {
      "success": true,
      "id": 52
  }
  ```

#### Получение одного заказа

- **URL**: `/api/orders/get/<int:id>/`
- **Метод**: POST
- **Пример ответа**:
  ```json
  {
      "client": {
          "id": 101,
          "full_name": "Иван Иванов",
          "email": "ivanov@example.com",
          "mobile_phone": "+79001234567"
      },
      "product": "Ноутбук",
      "quantity": 2,
      "price": "1500.00",
      "total_price": "3000.00",
      "description": "Заказ ноутбука",
      "status": "Pending",
      "created_at": "17.12.2024 21:00"
  }
  ```

#### Получение списка заказов

- **URL**: `/api/orders/get/`
- **Метод**: POST
- **Пример запроса**:
  ```json
  {
      "start_id": 0,  // Количество уже загруженных заказов
      "status": "Pending",  // Статус заказа
      "order_by": "-id",  // Сортировка по ID в порядке убывания
      "client_id": 101,  // Указывается при необходимости посмотреть заказы определенного клиента
      "search": "Ноутбук"  // Поиск по наименованию
  }
  ```
- **Пример ответа**:
  ```json
  {
      "orders": [
          {
              "id": 1,
              "client": {
                  "id": 101,
                  "full_name": "Иван Иванов",
                  "email": "ivanov@example.com",
                  "mobile_phone": "+79001234567"
              },
              "product": "Ноутбук",
              "quantity": 2,
              "price": "1500.00",
              "total_price": "3000.00",
              "description": "Заказ ноутбука",
              "status": "Pending",
              "created_at": "17.12.2024 21:00"
          }
      ]
  }
  ```

#### Редактирование заказа

- **URL**: `/api/orders/edit/<int:id>/`
- **Метод**: POST
- **Пример запроса**:
  ```json
  {
      "product": "Смартфон",
      "quantity": 3,
      "price": "1000.00",
      "status": "Completed"
  }
  ```
- **Пример ответа**:
  ```json
  {
      "success": true,
      "id": 52
  }
  ```

#### Удаление заказа

- **URL**: `/api/orders/delete/<int:id>/`
- **Метод**: DELETE
- **Пример ответа**:
  ```json
  {
      "success": true
  }
  ```

---

### Работа с отчетами

#### Создание отчета
- **URL**: `/api/reports/new/`
- **Метод**: POST
- **Пример запроса**:
  ```json
  {
      "period": "week", // week, month, year
  }
  ```
- **Пример ответа**:
  ```json
  {
      "success": true,
      "id": 12
  }
  ```

#### Получение всех отчетов
- **URL**: `/api/reports/get/`
- **Метод**: GET
- **Пример ответа**:
  ```json
  {
      "reports": [
          {
              "id": 1,
              "period": "month",
              "new_orders_count": 10,
              "new_clients_count": 5,
              "total_orders_sum": "5000.00",
              "avg_order_sum": "500.00",
              "completed_orders_count": 8,
              "date_created": "17 декабря 2024 года, 21:00"
          }
      ]
  }
  ```

#### Получение отчета по ID
- **URL**: `/api/reports/get/<int:id>/`
- **Метод**: GET
- **Пример ответа**:
  - **Тип контента**: `text/plain`
  - **Файл**: `report_<id>.txt`
  - Ответ будет содержать файл с отчетом в текстовом формате, который можно загрузить.

---

## Диаграммы

![0f54e6a3-1288-4942-af13-1a199f60ddb6](https://github.com/user-attachments/assets/ee138014-7332-4d39-8043-bb5373d8bf3e)

![ab5f78ee-00d1-46d7-9997-1e62b2702a0e](https://github.com/user-attachments/assets/3092049d-0478-431a-8787-3df6668e03cc)

![24eda96c-90fe-4006-87cb-f609d0035565](https://github.com/user-attachments/assets/7f72f423-c3bd-4375-9975-491b939da00a)

![9b874125-ca58-4437-ad16-b085794f83ab](https://github.com/user-attachments/assets/e93c868a-64b9-4634-8448-557b19701e9c)

---

## Технологический стек

- **Backend и API**: Django, Django Rest Framework, Django ORM, sqlite3
- **DevOps**: VDS Ubuntu 22.04, Gunicorn, Nginx, Git
- **Frontend**: HTML, CSS, JS
- **Мобильное приложение**: Kotlin, Jetpack Compose, Coroutines

## Участники проекта

- **Руслан Онищенко ([ober0](https://github.com/ober0))** - _Ведущий разработчик, Backend-разработчик, Frontend-разработчик, DevOps_
- **Панкратов Александр**  - _Разработчик мобильного приложения (Kotlin)_
- **Осипов Максим** - _Frontend-разработчик_
- **Алексеев Владислав** - _UX/UI-дизайнер, документатор_
- **Мордик Владислав** - _UX/UI-дизайнер_
- **Анатолий Тюрин** - _Документатор, разработчик диаграмм_
```
