document.getElementById('vehicle-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const responseMessage = document.getElementById('response-message');
    responseMessage.textContent = 'Submitting...';
    responseMessage.style.color = '#007BFF';

    try {
        const response = await fetch('/add_vehicle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            responseMessage.textContent = 'Vehicle registered successfully!';
            responseMessage.style.color = 'green';
            form.reset(); // Clear the form
        } else {
            responseMessage.textContent = `Error: ${result.error}`;
            responseMessage.style.color = 'red';
        }
    } catch (error) {
        responseMessage.textContent = 'An unexpected error occurred. Please try again.';
        responseMessage.style.color = 'red';
        console.error('Error:', error);
    }
});