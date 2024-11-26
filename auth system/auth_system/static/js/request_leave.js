// static/js/leave_request.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('leave-request-form');
    
    if (!form) {
        console.error('Form not found');
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const startDate = document.getElementById('start-date');
        const endDate = document.getElementById('end-date');

        if (!startDate?.value || !endDate?.value) {
            alert('Please fill all required fields');
            return;
        }

        try {
            const response = await fetch('/api/leave-requests/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    start_date: startDate.value,
                    end_date: endDate.value
                })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || Object.values(data)[0][0]);
            }

            alert('Leave request submitted successfully');
            window.location.href = '/attendance';
        } catch (error) {
            alert(error.message || 'Failed to submit leave request');
        }
    });
});