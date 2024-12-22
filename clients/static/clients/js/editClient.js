fetch(`/api/clients/get/${document.querySelector('input[name="client_id"]').value}/`, {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
    }
})
.then(response => {
    if (!response.ok) {
        console.error('Ошибка HTTP:', response.status);
        throw new Error('Ошибка при запросе данных');
    }
    return response.json();
})
.then(result => {
    const client = result.client;
    document.getElementById('first_name').value = client.first_name || '';
    document.getElementById('middle_name').value = client.middle_name || '';
    document.getElementById('last_name').value = client.last_name || '';
    document.getElementById('email').value = client.email || '';
    document.getElementById('mobile_phone').value = client.mobile_phone || '';
})
.catch(error => console.error('Ошибка при загрузке данных:', error));

document.getElementById('client-form-send').addEventListener('click', function () {
    const formData = new FormData(document.getElementById('client-form'));

    // Отправляем данные на сервер
    fetch(`/api/clients/edit/${document.querySelector('input[name="client_id"]').value}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            window.location.href = `/clients/${result.id}/`;
        } else {
            alert('Ошибка при сохранении данных клиента');
        }
    })
    .catch(error => console.error('Ошибка при обновлении данных:', error));
});