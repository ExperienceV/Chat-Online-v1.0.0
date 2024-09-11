document.addEventListener('DOMContentLoaded', async function() {
    const ws = new WebSocket("ws://" + window.location.host + "/ws_chat");
    const form = document.getElementById('send-message');
    const messageInput = document.getElementById('message');
    const messageList = document.getElementById('messages');
    const token = sessionStorage.getItem('token');


    function create_msg(type, message) {
        const newMessage = document.createElement('li');
        newMessage.className = type;
        newMessage.textContent = `${message}`; 
        messageList.appendChild(newMessage);
        messageList.scrollTop = messageList.scrollHeight;
    }

    function delete_div(id_div) {
        const div = document.getElementById(id_div);
        if (div) {
            div.remove();
        }
    }

    function token_not_found() {
        const mensaje = document.createElement('p');
        
        mensaje.textContent = 'No estás autenticado correctamente';
        
        mensaje.style.fontFamily = 'Times New Roman, Times, serif';
        mensaje.style.fontStyle = 'italic'; 
        mensaje.style.color = 'red';
        mensaje.style.fontSize = '50px';
        mensaje.style.textAlign = 'center';
        mensaje.style.marginTop = '20px';
        
        document.body.appendChild(mensaje);
    }
    
    async function loadMessages() {
        try {
            const data = await fetchData('http://localhost:8000/load_messages');
            console.log(data);

            data.forEach((msg) => {
                if (msg.startsWith('true')) {
                    create_msg('message sent', msg.substring(5).trim());

                } else if (msg.startsWith('false')) {
                    create_msg('message received', msg.substring(5).trim());

                }
            });

        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    async function fetchData(url) {
        const response = await fetch(url, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
            delete_div('chat_div')
            token_not_found()
            throw new Error(`HTTP error! status: ${response.status}`)
        };

        
        return response.json();

        
    }

    async function fetchChat() {
        try {
            await fetchData('http://localhost:8000/chat_request');
            loadMessages();
        } catch (error) {
            console.error('Error fetching chat:', error);
        }
    }

    
    fetchChat();
    

    let lastSentMessage = '';

    ws.onmessage = function(event) {
        const receivedMessage = event.data;
        if (receivedMessage !== lastSentMessage) {
            const newMessage = document.createElement('li');
            newMessage.className = 'message received';
            newMessage.textContent = `${receivedMessage}`; 
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