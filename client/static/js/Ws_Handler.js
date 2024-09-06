document.addEventListener('DOMContentLoaded', async function() {
    const ws = new WebSocket("ws://" + window.location.host + "/ws_chat");
    const form = document.getElementById('send-message');
    const messageInput = document.getElementById('message');
    const messageList = document.getElementById('messages');
    const token = sessionStorage.getItem('token')


    async function addFrame() {
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

    fetchChat();


    // Cargar mensajes guardados.
    try {
        const response = await fetch('http://localhost:8000/load_messages', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = response.json();
        console.log(data);

    } catch (error) {
        console.error('Error al realizar el fetch:', error);
    }



    // Variable para almacenar el último mensaje enviado
    let lastSentMessage = '';

    ws.onmessage = function(event) {
        const receivedMessage = event.data;

        // Verificar si el mensaje recibido es diferente al último mensaje enviado
        if (receivedMessage !== lastSentMessage) {
            const newMessage = document.createElement('li');
            newMessage.className = 'message received';
            newMessage.textContent = receivedMessage;
            messageList.appendChild(newMessage);
            messageList.scrollTop = messageList.scrollHeight; // Scroll to bottom
        }
    };

    form.onsubmit = function(e) {
        e.preventDefault();
        const messageText = messageInput.value;
        

        // Crear y añadir el mensaje enviado a la lista
        const sentMessage = document.createElement('li');
        sentMessage.className = 'message sent';
        sentMessage.textContent = messageText;
        messageList.appendChild(sentMessage);
        messageList.scrollTop = messageList.scrollHeight; // Scroll to bottom

        try {
            // Enviar mensaje a través del WebSocket
            const data_send = {
                "token" : token,
                "message" : messageText
            } 
            ws.send(JSON.stringify(data_send));
            console.log(data_send)
            console.log(typeof(data_send))
            // Almacenar el mensaje enviado para comparación
            lastSentMessage = messageText;

            messageInput.value = '';
        } catch (error) {
            console.log(error)
            
        }
    };
});


