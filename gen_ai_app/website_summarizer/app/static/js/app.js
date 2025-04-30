document.addEventListener('DOMContentLoaded', function() {
    // Add event listener for Send button
    const sendButton = document.getElementById('send-button');
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    // Add event listener for Summarize button
    const summarizeButton = document.getElementById('summarize-button');
    if (summarizeButton) {
        summarizeButton.addEventListener('click', summarizeUrl);
    }
});

async function sendMessage() {
    const model = document.getElementById('model').value;
    const message = document.getElementById('message').value;
    if (!message.trim()) return;
    // Append user message to chat box (bubble design)
    const chatBox = document.getElementById('chat-box');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'chat-message user';
    userMessageDiv.innerHTML = `
        <div>${marked.parse(message)}</div>
        <div class="chat-meta">You・${new Date().toLocaleTimeString()}</div>
    `;
    chatBox.appendChild(userMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    // 1. Send to AI
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model, message, thread_id: window.currentThreadId }),
    });
    const data = await response.json();
    // 2. Display AI response (bubble design)
    const aiMessageDiv = document.createElement('div');
    aiMessageDiv.className = 'chat-message ai';
    if (data.error) {
        aiMessageDiv.innerHTML = `<div>Error - ${data.error}</div><div class="chat-meta">AI・${new Date().toLocaleTimeString()}</div>`;
    } else {
        aiMessageDiv.innerHTML = `<div>${marked.parse(data.message)}</div><div class="chat-meta">AI・${new Date().toLocaleTimeString()}</div>`;
    }
    chatBox.appendChild(aiMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    // 3. Save thread via API
    if (!window.currentThreadId) {
        // Create new thread (send the first exchange)
        const res = await fetch('/threads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({
                text: message,
                ai_text: data.message
            }),
        });
        if (res.ok) {
            const thread = await res.json();
            window.currentThreadId = thread.id;
            await loadThreads(); // Reload only on new creation
        }
    } else {
        // Add to existing thread
        await fetch(`/threads/${window.currentThreadId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({
                text: message,
                ai_text: data.message
            }),
        });
    }
    document.getElementById('message').value = '';
}


async function summarizeUrl() {
    const url = document.getElementById('url-input').value;
    if (!url) return;
    const chatBox = document.getElementById('chat-box');
    
    // Add user message in bubble chat design
    chatBox.innerHTML += `
        <div class="chat-message user">
            <div>${marked.parse(url)}</div>
            <div class="chat-meta">You・${new Date().toLocaleTimeString()}</div>
        </div>
    `;
    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, thread_id: window.currentThreadId })
        });
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.indexOf('application/json') !== -1) {
            const data = await response.json();
            if (data.summary) {
                // Add AI message in bubble chat design
                chatBox.innerHTML += `
                    <div class="chat-message ai">
                        <div>${marked.parse(data.summary)}</div>
                        <div class="chat-meta">AI・${new Date().toLocaleTimeString()}</div>
                    </div>
                `;
                if (data.thread_id) {
                    window.currentThreadId = data.thread_id;
                }
                // Reload the thread list immediately after summarization
                if (typeof loadThreads === 'function') {
                    loadThreads();
                }
            } else {
                chatBox.innerHTML += `<div class='error-message'>Error: ${data.error}</div>`;
            }
        } else {
            const text = await response.text();
            chatBox.innerHTML += `<div class='error-message'>Server error: ${text}</div>`;
        }
    } catch (error) {
        chatBox.innerHTML += `<div class='error-message'>Error: ${error.message}</div>`;
    }
    document.getElementById('url-input').value = '';
}

window.summarizeUrl = summarizeUrl;
