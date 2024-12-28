document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#update-admission-group-form');
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const url = form.action;

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message); 
            } else if (data.errors) {
                alert('Error: ' + JSON.stringify(data.errors)); 
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
