document.addEventListener('DOMContentLoaded', () => {
    
    const form = document.querySelector('.form-container form');     
    const nameInput = form.querySelector('#name');
    const emailInput = form.querySelector('#email');
    const mobileInput = form.querySelector('#mobile');
    const dateInput = form.querySelector('#date');
    const timeInput = form.querySelector('#time');
    const addressInput = form.querySelector('#address');
    const wasteInput = form.querySelector('#waste');
    const quantityInput = form.querySelector('#quantity');

    form.addEventListener('submit', (e) => {
        
        resetErrors(form);

        let valid = true;

        if (!nameInput.value.trim()) {
            showError(nameInput, "Name is required.");
            valid = false;
        }

        if (!emailInput.value.trim() || !validateEmail(emailInput.value)) {
            showError(emailInput, "A valid email is required.");
            valid = false;
        }

        if (!mobileInput.value.trim()) {
            showError(mobile, "Mobile number is required.");
            valid = false;
        } else if (!/^\d{10}$/.test(mobileInput.value)) {
            showError(mobileInput, "Enter a valid 10-digit mobile number.");
            valid = false;
        }

        if (!dateInput.value.trim()) {
            showError(dateInput, "Pickup date is required.");
            valid = false;
        }

        if (!timeInput.value.trim()) {
            showError(timeInput, "Pickup time is required.");
            valid = false;
        }

        if (!addressInput.value.trim()) {
            showError(addressInput, "Pickup address is required.");
            valid = false;
        }

        if (!wasteInput.value.trim()) {
            showError(wasteInput, "Waste type is required.");
            valid = false;
        }

        if (!quantityInput.value.trim() || quantityInput.value <= 0) {
            showError(quantityInput, "Valid quantity is required.");
            valid = false;
        }

        if (!valid) {
            e.preventDefault(); // Only prevent submission when invalid
        }
    });

    // Utility function to show error
    function showError(input, message) {
        const errorDiv = input.nextElementSibling;
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.color = "red";
        }
        input.style.borderColor = "red";
    }

    // Utility function to reset all errors
    function resetErrors(form) {
        const errorElements = form.querySelectorAll('.error');
        errorElements.forEach((errorDiv) => {
            errorDiv.textContent = "";
        });

        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach((input) => {
            input.style.borderColor = "";
        });
    }

    // Utility function to validate email
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});
