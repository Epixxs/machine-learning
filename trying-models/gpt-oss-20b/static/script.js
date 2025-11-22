document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;


        addMessage(message, 'user');
        userInput.value = '';


        const loadingId = addLoadingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();


            removeMessage(loadingId);


            addMessage(data.response, 'ai');
        } catch (error) {
            console.error('Error:', error);
            removeMessage(loadingId);
            addMessage('Sorry, something went wrong. Please try again.', 'ai');
        }
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = sender === 'user' ? 'You' : 'AI';

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('content');
        contentDiv.textContent = text;

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        chatContainer.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv.id = 'msg-' + Date.now();
    }

    function addLoadingIndicator() {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'ai-message');
        messageDiv.id = 'loading-' + Date.now();

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = 'AI';

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('typing-indicator');

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            contentDiv.appendChild(dot);
        }

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        chatContainer.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv.id;
    }

    function removeMessage(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
