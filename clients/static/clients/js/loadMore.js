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
        const parentEl = document.querySelector('#clients-list');
        const rows = parentEl ? parentEl.querySelectorAll('tr') : [];
        let start_id = 0;

        if (rows.length > 0) {
            start_id = rows.length
        }

        const searchValue = document.getElementById('search').value;

        if (searchValue && searchValue !== '') {
            formData.append('search', searchValue);
        }

        formData.append('start_id', start_id);
        formData.append('order_by', currentOrderBy);

        fetch('/api/clients/get/', {
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
                if (!result.clients || result.clients.length === 0) {
                    noMoreData = true;
                    return;
                }

                const existingIds = new Set(
                    Array.from(parentEl.querySelectorAll('tr')).map(row => parseInt(row.id))
                );

                const clientsHtml = result.clients
                    .filter(client => !existingIds.has(client.id))
                    .map((client) => {
                        return ` 
                            <tr id="${client.id}">
                                <td>${client.id}</td>
                                <td>${client.last_name}</td>
                                <td>${client.first_name}</td>
                                <td>${client.middle_name}</td>
                                <td>${client.mobile_phone}</td>
                                <td>${client.email}</td>
                            </tr>
                        `;
                    })
                    .join('');

                if (parentEl) {
                    parentEl.insertAdjacentHTML('beforeend', clientsHtml);

                    // Обработчик клика по строкам таблицы
                    const rows = parentEl.querySelectorAll('tr');
                    rows.forEach(row => {
                        row.addEventListener('click', function () {
                            const clientId = row.id;
                            window.location.href = `/clients/${clientId}/`;  // Переход на страницу с деталями клиента
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
        const parentEl = document.querySelector('#clients-list');
        if (parentEl) {
            parentEl.innerHTML = '';
        }

        noMoreData = false;
        loadClients();
    });

    document.getElementById('search').addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {  // Если нажата клавиша Enter
            const parentEl = document.querySelector('#clients-list');
            if (parentEl) {
                parentEl.innerHTML = '';
            }

            noMoreData = false;
            loadClients();
        }
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

            const parentEl = document.querySelector('#clients-list');
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
