document.getElementById('send-button').addEventListener('click', async () => {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class='user-message'>${userInput}</div>`;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput }),
        });

        const data = await response.json();
        if (data.message) {
            chatBox.innerHTML += `<div class='ai-message'>${data.message}</div>`;
        } else {
            chatBox.innerHTML += `<div class='error-message'>Error: ${data.error}</div>`;
        }
    } catch (error) {
        chatBox.innerHTML += `<div class='error-message'>Error: ${error.message}</div>`;
    }

    document.getElementById('user-input').value = '';
});
