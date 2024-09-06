const resultDiv = document.getElementById('result');    
const token = sessionStorage.getItem('token')
console.log('Token obtenido: ' + token)

function addFrame() {
    const chat_frame = document.createElement('iframe');
    const container = document.getElementById('container')

    chat_frame.src = 'static/html/test.html';
    chat_frame.id = 'chat_frame';
    chat_frame.title = 'CHAT'
    chat_frame.width = '100%';
    chat_frame.height = '100vh';
    
    container.appendChild(chat_frame)
}

async function fetchChat() {
    try {
        const response = await fetch('http://localhost:8000/chat_request', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json()

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${JSON.stringify(data.detail)}`);
        }

        
        resultDiv.remove();
        addFrame();
        
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    }
}



// Realizar el fetch automáticamente al cargar la página
fetchChat();