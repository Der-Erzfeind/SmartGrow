function openModal(modalId) {
    document.getElementById(modalId).style.display = "flex";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

function validateForm() {
    const password = document.getElementById('password_register').value;
    const confirmPassword = document.getElementById('confirm_password_register').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match. Please try again.');
        return false;
    }
    return true;
}

async function handleRegister(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.success);
            closeModal('registerModal');
        } else {
            alert(result.error);
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData
        });

        if (response.status === 401) {
            const result = await response.json();
            alert(result.error);
        } else if (response.ok) {
            window.location.href = "/dashboard";
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}
