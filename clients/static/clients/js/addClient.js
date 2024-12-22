document.getElementById('create-client-btn').addEventListener('click', function () {
    const form = document.getElementById('create-client-form');

    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }

    const firstName = document.getElementById('first_name').value;
    const middleName = document.getElementById('middle_name').value;
    const lastName = document.getElementById('last_name').value;
    const email = document.getElementById('email').value;
    const mobilePhone = document.getElementById('mobile_phone').value;

    const formData = new FormData();
    formData.append('first_name', firstName);
    formData.append('middle_name', middleName);
    formData.append('last_name', lastName);
    formData.append('email', email);
    formData.append('mobile_phone', mobilePhone);

    fetch('/api/clients/add/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        }
    })
    .then(response => response.json())
    .then(result => {
        if (!result.success){
            if (result.error === 'Email already registered.'){
                $('#alreaderegisteredModal').modal('show');
                document.getElementById('redirect-client').addEventListener('click', function() {
                    window.location.href = `/clients/${result.id}/`;
                });
            }
        }
        else {
            window.location.href = `/clients/${result.id}/`;
        }

    })
    .catch(error => {
        console.error('Ошибка при отправке данных:', error);
    });
});