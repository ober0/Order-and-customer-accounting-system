function fetchReports() {
    fetch('/api/reports/get/')
        .then(response => response.json())
        .then(data => {
            const reportListContainer = document.getElementById('reportList');
            reportListContainer.innerHTML = '';

            data.reports.forEach(report => {
                const reportItem = document.createElement('div');
                reportItem.classList.add('report-item', 'mb-3', 'p-3', 'border', 'rounded');

                let period_ru = 'месяц'
                switch (report.period){
                    case 'week':
                        period_ru = 'неделю'
                        break
                    case 'month':
                        period_ru = 'месяц'
                        break
                    case 'year':
                        period_ru = 'год'
                        break
                }

                reportItem.innerHTML = `
                    <h3>Отчет за ${period_ru}</h3>
                    <p><strong>Дата создания:</strong> ${report.date_created}</p>
                    <button class="btn btn-success" onclick="downloadReport(${report.id})">Скачать файл</button>
                `;
                reportListContainer.appendChild(reportItem);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке отчетов:', error);
        });
}

function createReport() {
    const period = document.getElementById('reportPeriod').value;
    let formData = new FormData();
    formData.append('period', period);

    fetch('/api/reports/new/', {
        method: 'POST',
        headers: {
            'X-CSRFtoken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
        body: formData
    })
    .then(response => {
        window.location.reload();
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function downloadReport(reportId) {
    fetch(`/api/reports/get/${reportId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `report_${reportId}.txt`;
        link.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

window.onload = fetchReports;