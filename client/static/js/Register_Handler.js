async function submitForm(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = {
      user_name: formData.get('user_name'),
      user_password: formData.get('user_password'),
      confirm_password: formData.get('confirm_password')
    };
    const responseElement = document.getElementById('response'); // Asegúrate de tener este elemento en el HTML
    try {
      const response = await fetch('http://localhost:8000/register_request', {
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

        sessionStorage.setItem('token', result.detail)
        window.location.href = "/chat"

      } catch (error) {
        responseElement.textContent = error.message;
        responseElement.className = 'alert alert-danger';
      }
    }