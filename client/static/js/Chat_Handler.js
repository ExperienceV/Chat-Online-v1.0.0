const resultDiv = document.getElementById('result');    
const token = sessionStorage.getItem('token');
console.log('Token obtenido: ' + token);

function addFrame() {
    const chat_frame = document.createElement('iframe');
    chat_frame.src = 'static/html/chat.html';
    chat_frame.id = 'chat_frame';
    chat_frame.title = 'CHAT';
    chat_frame.width = '100%';
    chat_frame.height = '100vh';
    document.getElementById('container').appendChild(chat_frame);
}

async function fetchData(url) {
    const response = await fetch(url, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) {
        const data = await response.json();
        throw new Error(`HTTP error! status: ${JSON.stringify(data.detail)}`);
    }
    return response.json();
}

async function fetchChat() {
    try {
        await fetchData('http://localhost:8000/chat_request');
        resultDiv.remove();
        addFrame();
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    }
}

fetchChat();