document.addEventListener('DOMContentLoaded', async function() {
    const ws = new WebSocket("ws://" + window.location.host + "/ws_chat");
    const form = document.getElementById('send-message');
    const messageInput = document.getElementById('message');
    const messageList = document.getElementById('messages');
    const token = sessionStorage.getItem('token');
    
    async function addFrame() {
        const chat_frame = document.createElement('iframe');
        chat_frame.src = 'static/html/test.html';
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
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    }

    async function fetchChat() {
        try {
            await fetchData('http://localhost:8000/chat_request');
            addFrame();
        } catch (error) {
            console.error('Error fetching chat:', error);
        }
    }

    async function loadMessages() {
        try {
            const data = await fetchData('http://localhost:8000/load_messages');
            console.log(data);
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    fetchChat();
    loadMessages();

    let lastSentMessage = '';

    ws.onmessage = function(event) {
        const receivedMessage = event.data;
        if (receivedMessage !== lastSentMessage) {
            const newMessage = document.createElement('li');
            newMessage.className = 'message received';
            newMessage.textContent = receivedMessage;
            newMessage.textContent = `${msg.message} (Recibido: ${msg.timestamp})`;
            messageList.appendChild(newMessage);
            messageList.scrollTop = messageList.scrollHeight;
        }
    };

    form.onsubmit = function(e) {
        e.preventDefault();
        const messageText = messageInput.value;
        const sentMessage = document.createElement('li');
        sentMessage.className = 'message sent';
        sentMessage.textContent = messageText;
        newMessage.textContent = `${msg.message} (Enviado: ${msg.timestamp})`;
        messageList.appendChild(sentMessage);
        messageList.scrollTop = messageList.scrollHeight;

        try {
            ws.send(JSON.stringify({ token, message: messageText }));
            lastSentMessage = messageText;
            messageInput.value = '';
        } catch (error) {
            console.log('Error sending message:', error);
        }
    };
});