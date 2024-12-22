function sendData(){
    const client = document.getElementById('client').value;
        const product = document.getElementById('product').value;
        const quantity = document.getElementById('quantity').value;
        const price = document.getElementById('price').value;
        const description = document.getElementById('description').value;


        const formData = new FormData();
        formData.append('client', client);
        formData.append('product', product);
        formData.append('quantity', quantity);
        formData.append('price', price);
        formData.append('description', description);

        fetch('/api/orders/add/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
            }
        })
        .then(response => response.json())
        .then(result => {
            window.location.href = `/orders/${result.id}/`;

        })
        .catch(error => {
            console.error('Ошибка при отправке данных:', error);
        });
}

document.getElementById('add-new-client-btn').addEventListener('click', function () {
    window.location.href = '/clients/add/?next=/orders/add/';
});

document.getElementById('select-existing-client-btn').addEventListener('click', function () {
    $('#selectClientModal').modal('show');
    loadClients();
});

document.getElementById('create-order-btn').addEventListener('click', function () {
    const form = document.getElementById('create-order-form');
    const clientField = document.getElementById('client');
    const clientNameField = document.getElementById('client-name');

    if (!clientField.value) {
        clientNameField.setCustomValidity('Клиент обязателен.');
    } else {
        clientNameField.setCustomValidity('');
    }

    if (form.checkValidity()) {
        sendData()
    } else {
        form.classList.add('was-validated');
        clientNameField.reportValidity();
    }
});


let isLoadingClients = false;
let noMoreClients = false;

function loadClients() {
    if (isLoadingClients || noMoreClients) return;

    isLoadingClients = true;

    const clientList = document.getElementById('client-list');
    const rows = clientList ? clientList.querySelectorAll('tr') : [];
    const startId = rows.length;
    const searchValue = document.getElementById('client-search').value;

    let formData = new FormData();
    formData.append('start_id', startId);
    formData.append('search', searchValue);
    formData.append('order_by', '-id');
    fetch(`/api/clients/get/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.clients || data.clients.length === 0) {
                noMoreClients = true;
                return;
            }

            const clientsHtml = data.clients.map(client => `
                <tr data-id="${client.id}" data-name="${client.last_name} ${client.first_name} ${client.middle_name}" class="selectable-client">
                    <td>${client.id}</td>
                    <td>${client.first_name}</td>
                    <td>${client.last_name}</td>
                    <td>${client.middle_name}</td>
                    <td>${client.mobile_phone}</td>
                    <td>${client.email}</td>
                </tr>
            `).join('');

            clientList.insertAdjacentHTML('beforeend', clientsHtml);

            document.querySelectorAll('.selectable-client').forEach(row => {
                row.addEventListener('click', function () {
                    const clientId = row.getAttribute('data-id');
                    document.getElementById('client').value = clientId;
                    const clientFullName = row.getAttribute('data-name');
                    document.getElementById('client-name').value = clientFullName;
                    $('#selectClientModal').modal('hide');
                });
            });
        })
        .catch(error => console.error('Ошибка загрузки клиентов:', error))
        .finally(() => {
            isLoadingClients = false;
        });
}

document.getElementById('client-search').addEventListener('input', function () {
    document.getElementById('client-list').innerHTML = '';
    noMoreClients = false;
    loadClients();
});

document.querySelector('#table').addEventListener('scroll', function () {
    const { scrollTop, scrollHeight, clientHeight } = this;
    if (scrollTop + clientHeight >= scrollHeight - 50 && !isLoadingClients && !noMoreClients) {
        loadClients();
    }
});