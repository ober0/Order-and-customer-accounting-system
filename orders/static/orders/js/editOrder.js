function updateTotalPrice() {
    const price = parseFloat(document.getElementById('price').value) || 0;
    const quantity = parseInt(document.getElementById('quantity').value) || 0;
    const totalPrice = price * quantity;
    document.getElementById('total_price').value = totalPrice.toFixed(2);
}

fetch(`/api/orders/get/${document.querySelector('input[name="order_id"]').value}/`, {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
    },
})
.then(response => response.json())
.then(result => {
    let fullName = result.client.client.full_name.split(' ')
    document.getElementById('client_last_name').value = fullName[0] || '';
    document.getElementById('client_first_name').value = fullName[1] || '';
    document.getElementById('client_middle_name').value = fullName[2] || '';

    document.getElementById('client_email').value = result.client.client.email;
    document.getElementById('client_phone').value = result.client.client.mobile_phone;
    document.getElementById('product').value = result.client.product;
    document.getElementById('quantity').value = result.client.quantity;
    document.getElementById('price').value = result.client.price;
    document.getElementById('total_price').value = result.client.total_price;
    document.getElementById('description').value = result.client.description;
    document.getElementById('status').value = result.client.status;
})
.catch(error => console.error('Ошибка при загрузке данных:', error));

document.getElementById('order-form-send').addEventListener('click', function () {
    const formData = new FormData(document.getElementById('order-form'));

    fetch(`/api/orders/edit/${document.querySelector('input[name="order_id"]').value}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.success){
            window.location.href = `/orders/${result.id}/`;
        } else {
            alert('Ошибка при сохранении заказа');
        }
    })
    .catch(error => console.error('Ошибка при сохранении:', error));
});