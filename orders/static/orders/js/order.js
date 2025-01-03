fetch(`/api/orders/get/${document.querySelector('input[name="order_id"]').value}/`, {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
    },
})
.then(response => response.json())
.then(result => {
    if (result.client) {
        const order = result.client;
        document.querySelector('.data').innerHTML = `
            <div class="order-details">
                <h3>Информация о <a href="/clients/${order.client.id}">клиенте #${order.client.id}</a></h3>
                <div class="form-group">
                    <label for="client_full_name"><strong>Имя:</strong></label>
                    <input type="text" class="form-control" id="client_full_name" value="${order.client.full_name}" readonly>
                </div>
                <div class="form-group">
                    <label for="client_email"><strong>Email:</strong></label>
                    <input type="email" class="form-control" id="client_email" value="${order.client.email}" readonly>
                </div>
                <div class="form-group">
                    <label for="client_mobile_phone"><strong>Телефон:</strong></label>
                    <input type="text" class="form-control" id="client_mobile_phone" value="${order.client.mobile_phone}" readonly>
                </div>

                <h2>Детали заказа #${order.id}</h2>
                <div class="form-group">
                    <label for="product"><strong>Продукт:</strong></label>
                    <input type="text" class="form-control" id="product" value="${order.product}" readonly>
                </div>
                <div class="form-group">
                    <label for="quantity"><strong>Количество:</strong></label>
                    <input type="number" class="form-control" id="quantity" value="${order.quantity}" readonly>
                </div>
                <div class="form-group">
                    <label for="price"><strong>Цена за единицу:</strong></label>
                    <input type="number" class="form-control" id="price" value="${order.price}" readonly>
                </div>
                <div class="form-group">
                    <label for="total_price"><strong>Общая стоимость:</strong></label>
                    <input type="number" class="form-control" id="total_price" value="${order.total_price}" readonly>
                </div>
                <div class="form-group">
                    <label for="description"><strong>Описание:</strong></label>
                    <textarea class="form-control" id="description" rows="3" readonly>${order.description}</textarea>
                </div>
                <div class="form-group">
                    <label for="status"><strong>Статус:</strong></label>
                    <input type="text" class="form-control" value="${order.status}" readonly>
                </div>
                <div class="form-group">
                    <label for="created_at"><strong>Создан:</strong></label>
                    <input type="text" class="form-control" id="created_at" value="${order.created_at}" readonly>
                </div>

            </div>
        `;
    } else {
        document.querySelector('.data').innerHTML = '<p>Заказ не найден.</p>';
    }
})
.catch(error => console.error('Ошибка:', error));

document.getElementById('delete-btn').addEventListener('click', function () {
    if (confirm("Вы уверены, что хотите удалить этот заказ?")) {
        fetch(`/api/orders/delete/${document.querySelector('input[name="order_id"]').value}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                window.location.href = '/orders/';
            } else {
                alert('Ошибка при удалении заказа');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    }
});