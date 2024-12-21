document.addEventListener('DOMContentLoaded', function () {
    let isLoading = false;
    let noMoreData = false;
    let currentOrderBy = '-id';

    function updateArrow(column, direction) {
        document.querySelectorAll('.arrow').forEach(arrow => {
            arrow.textContent = '';
        });
        const arrowElement = document.getElementById('arrow-' + column);
        if (direction === 'asc') {
            arrowElement.textContent = ' ↑';
        } else {
            arrowElement.textContent = ' ↓';
        }
    }

    function loadClients() {
        if (isLoading || noMoreData) return;

        isLoading = true;

        const formData = new FormData();
        const parentEl = document.querySelector('#orders-list');
        const rows = parentEl ? parentEl.querySelectorAll('tr') : [];
        let start_id = 0;

         if (rows.length > 0) {
            start_id = rows.length
        }

        const searchValue = document.getElementById('search').value;
        const statusSelect = document.getElementById('status');
        const status = statusSelect ? statusSelect.value || 'Pending' : 'Pending';

        if (searchValue && searchValue !== '') {
            formData.append('search', searchValue);
        }

        formData.append('start_id', start_id);
        formData.append('order_by', currentOrderBy);
        formData.append('status', status);

        fetch('/api/orders/get/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            },
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((result) => {
                if (!result.orders || result.orders.length === 0) {
                    noMoreData = true;
                    return;
                }

                const existingIds = new Set(
                    Array.from(parentEl.querySelectorAll('tr')).map(row => parseInt(row.id))
                );

                const ordersHtml = result.orders
                    .filter(order => !existingIds.has(order.id))
                    .map((order) => {
                        let statusClass = '';
                        let statusText = '';
                        switch (order.status) {
                            case 'Pending':
                                statusClass = 'status-active';
                                statusText = 'В ожидании';
                                break;
                            case 'Completed':
                                statusClass = 'status-completed';
                                statusText = 'Завершен';
                                break;
                            case 'Cancelled':
                                statusClass = 'status-cancelled';
                                statusText = 'Отменен';
                                break;
                        }

                        return ` 
                            <tr id="${order.id}">
                                <td>${order.id}</td>
                                <td>${order.product}</td>
                                <td>${order.quantity} шт</td>
                                <td>${order.price} руб</td>
                                <td>${order.total_price} руб</td>
                                <td>${order.client.full_name}</td>
                                <td><span class="status ${statusClass}">${statusText}</span></td>
                                <td>${order.created_at}</td>
                            </tr>
                        `;
                    })
                    .join('');

                if (parentEl) {
                    parentEl.insertAdjacentHTML('beforeend', ordersHtml);

                    const rows = parentEl.querySelectorAll('tr');
                    rows.forEach(row => {
                        row.addEventListener('click', function () {
                            const orderId = row.id;
                            window.location.href = `/orders/${orderId}/`;
                        });
                    });
                }
            })
            .catch((error) => {
                console.error('Ошибка при загрузке данных:', error);
            })
            .finally(() => {
                isLoading = false;
            });
    }

    loadClients();

    document.getElementById('search-go').addEventListener('click', function () {
        const parentEl = document.querySelector('#orders-list');
        if (parentEl) {
            parentEl.innerHTML = '';
        }

        noMoreData = false;
        loadClients();
    });

    // Обработчик события для нажатия клавиши Enter в поле ввода поиска
    document.getElementById('search').addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {  // Если нажата клавиша Enter
            const parentEl = document.querySelector('#orders-list');
            if (parentEl) {
                parentEl.innerHTML = '';
            }

            noMoreData = false;
            loadClients();
        }
    });

    document.getElementById('status').addEventListener('change', function () {
        const parentEl = document.querySelector('#orders-list');
        if (parentEl) {
            parentEl.innerHTML = '';
        }

        noMoreData = false;
        loadClients();
    });

    document.querySelectorAll('th[data-column]').forEach((header) => {
        header.addEventListener('click', function () {
            const column = header.getAttribute('data-column');
            const currentDirection = currentOrderBy.startsWith('-') ? 'desc' : 'asc';

            if (currentDirection === 'asc') {
                currentOrderBy = `-${column}`;
                updateArrow(column, 'desc');
            } else {
                currentOrderBy = column;
                updateArrow(column, 'asc');
            }

            const parentEl = document.querySelector('#orders-list');
            if (parentEl) {
                parentEl.innerHTML = '';
            }

            noMoreData = false;
            loadClients();
        });
    });

    window.addEventListener('scroll', function () {
        if (
            window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 &&
            !isLoading &&
            !noMoreData
        ) {
            loadClients();
        }
    });
});
