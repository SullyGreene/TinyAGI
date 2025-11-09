const chatWindow = document.getElementById('chat-window-inner');
const promptInput = document.getElementById('prompt-input');
const sendButton = document.getElementById('send-button');
const stopButton = document.getElementById('stop-button');

/**
 * Adds a message to the chat UI.
 * @param {'user' | 'assistant'} role - The role of the message sender.
 * @param {string} content - The message content.
 */
export function addMessageToUI(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';

    // For user messages, we just set text content to avoid any HTML injection.
    // For assistant messages, we will parse markdown.
    if (role === 'user') {
        contentDiv.textContent = content;
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        contentDiv.dataset.rawText = content; // Store raw text for copying
        contentDiv.appendChild(copyButton);
    } else {
        // For assistant, we can put a placeholder or leave it empty,
        // as it will be populated by the streaming update function.
        contentDiv.innerHTML = content;
        // Raw text for assistant messages is added during update.
    }
    
    messageDiv.appendChild(contentDiv);
    chatWindow.appendChild(messageDiv); // chatWindow is now chat-window-inner
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

/**
 * Shows the "thinking" indicator and returns the element for live updates.
 * @returns {HTMLElement} The content element of the assistant's message.
 */
export function showThinkingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content thinking';
    // Create the typing indicator structure
    contentDiv.innerHTML = `<div class="typing-indicator">
                                <span></span><span></span><span></span>
                            </div>`;
    
    messageDiv.appendChild(contentDiv);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    
    return contentDiv; // Return the element that will be updated
}

/**
 * Updates the streaming assistant message.
 * @param {HTMLElement} contentDiv - The content element to update.
 * @param {string} fullResponseHtml - The full response text (already parsed as HTML) to display.
 */
export function updateAssistantMessage(contentDiv, fullResponseHtml) {
    // Remove thinking style on first update
    if (contentDiv.classList.contains('thinking')) {
        contentDiv.classList.remove('thinking');
        contentDiv.innerHTML = ''; // Clear "thinking..." indicator
    }
    // WARNING: Using innerHTML can be risky if the source is not trusted.
    // Since we control the AI, we accept this risk for rich formatting.
    // For production apps with external sources, use a sanitizer like DOMPurify.
    contentDiv.innerHTML = fullResponseHtml;
    chatWindow.scrollTop = chatWindow.scrollHeight;
    contentDiv.dataset.rawText = contentDiv.innerText; // Update raw text for copying

    // Find all <pre> elements and add a copy button and apply highlighting
    contentDiv.querySelectorAll('pre').forEach((preElement) => {
        // Add copy button if it doesn't exist
        if (!preElement.querySelector('.copy-button')) {
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-button';
            copyButton.textContent = 'Copy';
            preElement.appendChild(copyButton);
        }
        // Apply syntax highlighting
        const codeBlock = preElement.querySelector('code');
        if (codeBlock && !codeBlock.classList.contains('hljs')) {
            window.hljs.highlightElement(codeBlock);
        }
    });
}

/**
 * Toggles the input form's disabled state.
 * @param {boolean} disabled - Whether to disable the form.
 */
export function setFormDisabled(disabled) {
    promptInput.disabled = disabled;
    sendButton.disabled = disabled || promptInput.value.trim() === '';
}

/**
 * Clears all messages from the chat window.
 */
export function clearChatWindow() {
    const chatWindowInner = document.getElementById('chat-window-inner');
    chatWindowInner.innerHTML = `
        <div id="welcome-screen">
            <div class="welcome-logo">🚀</div>
            <h1>Welcome to TinyAGI</h1>
            <p>Select an agent from the sidebar to begin.</p>
        </div>`;
}

/**
 * Toggles between the Send and Stop buttons.
 * @param {boolean} isGenerating - True if the AI is generating a response.
 */
export function toggleStopButton(isGenerating) {
    sendButton.style.display = isGenerating ? 'none' : 'flex';
    stopButton.style.display = isGenerating ? 'flex' : 'none';
}

/**
 * Hides the welcome screen if it's visible.
 */
export function checkWelcomeScreen() {
    const welcomeScreen = document.getElementById('welcome-screen');
    if (welcomeScreen) {
        welcomeScreen.style.display = 'none';
    }
}

/**
 * Sets the active conversation in the history list.
 * @param {number | null} conversationId - The ID of the conversation to mark as active.
 */
export function setActiveConversation(conversationId) {
    const conversationItems = document.querySelectorAll('.conversation-item');
    conversationItems.forEach(item => {
        item.classList.remove('active');
        if (parseInt(item.dataset.id, 10) === conversationId) {
            item.classList.add('active');
        }
    });
}

/**
 * Populates the conversation history list in the sidebar.
 * @param {object[]} conversations - An array of conversation objects.
 * @param {number | null} activeConversationId - The ID of the currently active conversation.
 */
export function populateConversationHistory(conversations, activeConversationId) {
    const container = document.getElementById('conversation-history-container');
    if (!container) return;
    container.innerHTML = ''; // Clear previous list

    if (conversations.length === 0) {
        container.innerHTML = '<p class="history-empty-text">No chat history yet.</p>';
        return;
    }

    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        item.dataset.id = conv.id;
        if (conv.id === activeConversationId) {
            item.classList.add('active');
        }

        const title = document.createElement('span');
        title.textContent = conv.title;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-conversation-btn';
        deleteBtn.innerHTML = '&times;';
        deleteBtn.title = 'Delete conversation';

        item.appendChild(title);
        item.appendChild(deleteBtn);
        container.appendChild(item);
    });
}