const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadStatus = document.getElementById('upload-status');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const messagesContainer = document.getElementById('messages-container');
const resetBtn = document.getElementById('reset-btn');

// Reset Database
resetBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to delete all indexed documents? This cannot be undone.')) return;

    uploadStatus.textContent = 'Resetting database...';
    uploadStatus.className = 'status-msg loading';

    try {
        const response = await fetch('/reset', { method: 'POST' });
        if (response.ok) {
            uploadStatus.textContent = 'Database reset successfully!';
            uploadStatus.className = 'status-msg success';
            messagesContainer.innerHTML = `
                <div class="message bot">
                    <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                    <div class="content">
                        <p>Memory cleared! Upload a new document to start over.</p>
                    </div>
                </div>
            `;
        } else {
            throw new Error('Reset failed');
        }
    } catch (error) {
        uploadStatus.textContent = 'Error resetting database.';
        uploadStatus.className = 'status-msg error';
        console.error(error);
    }
});

// Drag and Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) handleUpload(files[0]);
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) handleUpload(fileInput.files[0]);
});

async function handleUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    uploadStatus.textContent = `Uploading ${file.name}...`;
    uploadStatus.className = 'status-msg loading';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            uploadStatus.textContent = 'Document indexed successfully!';
            uploadStatus.className = 'status-msg success';
            addMessage('bot', `I've finished reading **${file.name}**. You can now ask me questions about it!`);
        } else {
            throw new Error('Upload failed');
        }
    } catch (error) {
        uploadStatus.textContent = 'Error uploading file.';
        uploadStatus.className = 'status-msg error';
        console.error(error);
    }
}

// Generate Session ID
const sessionId = 'session-' + Math.random().toString(36).substr(2, 9);

// Chat Interaction
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage('user', text);
    userInput.value = '';

    // Loading indicator
    const loadingId = addLoadingMessage();

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: text,
                session_id: sessionId
            })
        });

        const data = await response.json();
        removeMessage(loadingId);

        if (response.ok) {
            addMessage('bot', data.answer, data.sources);
        } else {
            addMessage('bot', 'Sorry, I encountered an error processing your request.');
        }
    } catch (error) {
        removeMessage(loadingId);
        addMessage('bot', 'Network error. Please check your connection.');
        console.error(error);
    }
}

function addMessage(role, text, sources = []) {
    const div = document.createElement('div');
    div.className = `message ${role}`;

    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <details class="source-citation">
                <summary>View Sources</summary>
                <ul>
                    ${sources.map(s => `<li><strong>${s.source}</strong>: ${s.text.substring(0, 100)}...</li>`).join('')}
                </ul>
            </details>
        `;
    }

    // Simple markdown-like parsing for bold text
    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    div.innerHTML = `
        <div class="avatar">
            <i class="fa-solid ${role === 'bot' ? 'fa-robot' : 'fa-user'}"></i>
        </div>
        <div class="content">
            <p>${formattedText}</p>
            ${sourcesHtml}
        </div>
    `;

    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addLoadingMessage() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.className = 'message bot';
    div.id = id;
    div.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="content"><p><i class="fa-solid fa-circle-notch fa-spin"></i> Thinking...</p></div>
    `;
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
