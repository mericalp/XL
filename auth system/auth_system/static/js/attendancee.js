function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function setDefaultTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const timeString = `${hours}:${minutes}`; // HH:MM format

    document.getElementById('check-in-input').value = timeString;
    document.getElementById('check-out-input').value = timeString;
}

function submitAttendance() {
    const checkInTime = document.getElementById('check-in-input').value;
    const checkOutTime = document.getElementById('check-out-input').value;

    console.log('Submitting attendance:', checkInTime, checkOutTime); // Log ekleyin

    fetch('/api/attendance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            'check_in': checkInTime,
            'check_out': checkOutTime,
            'date': new Date().toISOString().split('T')[0]  // Tarihi ekleyin
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Attendance submitted successfully', data);
        document.getElementById('check-in-time').innerText = data.check_in;
        document.getElementById('check-out-time').innerText = data.check_out;
    })
    .catch(error => {
        console.error('Attendance submission failed', error);
    });
}

// Set default time on page load
document.addEventListener('DOMContentLoaded', setDefaultTime);