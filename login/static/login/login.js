document.querySelector('#submit').addEventListener('click', function () {
    const form = document.getElementById('userForm');
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;

    inputs.forEach(input => input.classList.remove('error'));

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
        }
    });

    if (!isValid) {
        document.getElementById('responseMessage').innerHTML =
            '<div class="alert alert-danger">Пожалуйста, заполните все обязательные поля.</div>';
        return;
    }

    const formData = new FormData(form);

    fetch('', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        window.location.reload()
    })
    .catch(error => {
        document.getElementById('responseMessage').innerHTML =
            `<div class="alert alert-danger">Произошла ошибка: ${error.message}</div>`;
    });
    });