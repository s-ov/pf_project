document.querySelector('#status-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const response = await fetch(this.action, {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();
    if (data.calendar_required) {
        alert(data.message);
        // Display calendar for user to select a deadline
        document.querySelector('#calendar').style.display = 'block';
    } else {
        alert(data.message);
        location.reload(); // Refresh page or redirect to task list
    }
});
