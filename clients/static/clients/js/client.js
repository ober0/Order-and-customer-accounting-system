fetch(`/api/clients/get/${document.querySelector('input[name="client_id"]').value}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
    })
    .then(response => response.json())
    .then(result => {
        if (result.client) {
            const client = result.client;
            document.querySelector('.data').innerHTML = `
                <div class="client-details">
                    <h2>Детали клиента #${client.id}</h2>
                    <div class="form-group">
                        <label for="client_name"><strong>ФИО:</strong></label>
                        <input type="text" class="form-control" id="client_name" value="${client.last_name} ${client.first_name} ${client.middle_name}" readonly>
                    </div>
                    <div class="form-group">
                        <label for="client_email"><strong>Email:</strong></label>
                        <input type="email" class="form-control" id="client_email" value="${client.email}" readonly>
                    </div>
                    <div class="form-group">
                        <label for="client_mobile_phone"><strong>Телефон:</strong></label>
                        <input type="text" class="form-control" id="client_mobile_phone" value="${client.mobile_phone}" readonly>
                    </div>
                </div>
            `;
        } else {
            document.querySelector('.data').innerHTML = '<p>Клиент не найден.</p>';
        }
    })
    .catch(error => console.error('Ошибка:', error));

    document.getElementById('delete-btn').addEventListener('click', function () {
        if (confirm("Вы уверены, что хотите удалить этого клиента? Будут удалены все связанные с ним заказы!")) {
            fetch(`/api/clients/delete/${document.querySelector('input[name="client_id"]').value}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                }
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    window.location.href = '/clients/';
                } else {
                    alert('Ошибка при удалении клиента');
                }
            })
            .catch(error => console.error('Ошибка:', error));
        }
    });