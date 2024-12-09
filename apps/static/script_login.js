function toggleForms() {
    const loginForm = document.querySelector('.login-form');
    const registerForm = document.querySelector('.register-form');
    
    loginForm.classList.toggle('inactive');
    registerForm.classList.toggle('active');
}

document.addEventListener("DOMContentLoaded", () => {
    // Select forms
    const loginForm = document.querySelector('.login-form form');
    const registerForm = document.querySelector('.register-form form');
    
    // Validation for login form
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Prevent form submission for validation
        const username = document.querySelector('form #username-login');
        const password = document.querySelector('.login-form #password-login');
        let valid = true;

        // Reset previous errors
        resetErrors(loginForm);

        if (!username.value.trim()) {
            showError(username, "Username is required.");
            valid = false;
        }

        if (!password.value.trim()) {
            showError(password, "Password is required.");
            valid = false;
        }

        if (valid) {
            loginForm.submit(); // Submit the form
        }
    });

    // Validation for register form
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Prevent form submission for validation
        const username = document.querySelector('.register-form #username');
        const email = document.querySelector('.register-form #email');
        const password = document.querySelector('.register-form #password1');
        const confirmPassword = document.querySelector('.register-form #password2');
        let valid = true;

        // Reset previous errors
        resetErrors(registerForm);

        if (!username.value.trim()) {
            showError(username, "Username is required.");
            valid = false;
        }

        if (!email.value.trim() || !validateEmail(email.value)) {
            showError(email, "A valid email is required.");
            valid = false;
        }

        if (!password.value.trim()) {
            showError(password, "Password is required.");
            valid = false;
        } else if (password.value.length < 4) {
            showError(password, "Password must be at least 4 characters.");
            valid = false;
        }

        if (confirmPassword.value !== password.value) {
            showError(confirmPassword, "Passwords do not match.");
            valid = false;
        }

        if (valid) {
            registerForm.submit(); // Submit the form
        }
    });

    // Utility functions
    function showError(input, message) {
        const errorDiv = input.nextElementSibling;
        errorDiv.textContent = message;
        errorDiv.style.color = "red";
        input.style.borderColor = "red";
    }

    function resetErrors(form) {
        const errors = form.querySelectorAll('.error');
        errors.forEach((error) => {
            error.textContent = "";
        });

        const inputs = form.querySelectorAll('input');
        inputs.forEach((input) => {
            input.style.borderColor = "";
        });
    }

    function showSuccess(form, message) {
        const messagesDiv = document.querySelector('.messages message');
        if (messagesDiv) {
            messagesDiv.innerHTML = `<div class="message">${message}</div>`;
            messagesDiv.style.color = "green";
            messagesDiv.style.border = "1px solid green";
        } else {
            alert(message);
        }
    }

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});
