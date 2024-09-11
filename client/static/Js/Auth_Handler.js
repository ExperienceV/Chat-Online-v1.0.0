async function handleRequest(url, data, responseElement) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail);
        }

        sessionStorage.setItem('token', result.detail);
        window.location.href = "/chat";

    } catch (error) {
        responseElement.textContent = error.message;
        responseElement.className = 'alert alert-danger';
    }
}

function getFormData(event) {
    const form = event.target;
    return new FormData(form);
}

async function registerFun(event) {
    event.preventDefault();
    const formData = getFormData(event);
    const data = {
        user_name: formData.get('user_name'),
        user_password: formData.get('user_password'),
        confirm_password: formData.get('confirm_password')
    };
    const responseElement = document.getElementById('response');
    await handleRequest('http://localhost:8000/register_request', data, responseElement);
}

async function loginFun(event) {
    event.preventDefault();
    const formData = getFormData(event);
    const data = {
        user_name: formData.get('user_name'),
        user_password: formData.get('user_password')
    };
    const responseElement = document.getElementById('response');
    await handleRequest('http://localhost:8000/authenticate_process', data, responseElement);
}