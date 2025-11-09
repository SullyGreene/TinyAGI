const agentSelect = document.getElementById('agent-select');
const chatWindow = document.getElementById('chat-window');
const promptInput = document.getElementById('prompt-input');
const sendButton = document.getElementById('send-button');
const stopButton = document.getElementById('stop-button');
const settingsModal = document.getElementById('settings-modal');
const agentModal = document.getElementById('agent-modal');
const editAgentModal = document.getElementById('edit-agent-modal');
const createAgentModal = document.getElementById('create-agent-modal');
const imageStudioModal = document.getElementById('image-studio-modal');
const ideStudioModal = document.getElementById('ide-studio-modal');
const roboticsStudioModal = document.getElementById('robotics-studio-modal');
const musicStudioModal = document.getElementById('music-studio-modal');
const videoStudioModal = document.getElementById('video-studio-modal');
const temperatureSlider = document.getElementById('temperature-slider');
const temperatureValue = document.getElementById('temperature-value');
const maxTokensSlider = document.getElementById('max-tokens-slider');
const maxTokensValue = document.getElementById('max-tokens-value');
const systemPromptTextarea = document.getElementById('system-prompt');
const themeToggleButton = document.getElementById('theme-toggle-button');
const sidebarToggleButton = document.getElementById('sidebar-toggle');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');

const THEME_KEY = 'tinyagi_theme';

/**
 * Applies the saved theme from localStorage or defaults to 'dark'.
 */
export function applyTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
    document.body.dataset.theme = savedTheme;
    updateThemeIcon(savedTheme);
}

/**
 * Toggles the color theme between 'light' and 'dark'.
 */
export function toggleTheme() {
    const currentTheme = document.body.dataset.theme || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.body.dataset.theme = newTheme;
    localStorage.setItem(THEME_KEY, newTheme);
    updateThemeIcon(newTheme);
}

/**
 * Updates the theme toggle button icon.
 * @param {string} theme - The current theme ('light' or 'dark').
 */
function updateThemeIcon(theme) {
    if (!themeToggleButton) return;
    const sunIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.64 5.64c-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41l1.06 1.06c.39.39 1.02.39 1.41 0s.39-1.02 0-1.41L5.64 5.64zm12.72 12.72c-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41l1.06 1.06c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41l-1.06-1.06zM5.64 18.36c.39.39.39 1.02 0 1.41-.39.39-1.02.39-1.41 0l-1.06-1.06c-.39-.39-.39-1.02 0-1.41s1.02-.39 1.41 0l1.06 1.06zm12.72-12.72c.39.39.39 1.02 0 1.41-.39.39-1.02.39-1.41 0l-1.06-1.06c-.39-.39-.39-1.02 0-1.41s1.02-.39 1.41 0l1.06 1.06z"/></svg>`;
    const moonIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-3.31 0-6-2.69-6-6 0-1.82.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>`;
    themeToggleButton.innerHTML = theme === 'dark' ? sunIcon : moonIcon;
}

const SIDEBAR_STATE_KEY = 'tinyagi_sidebar_state';

/**
 * Applies the saved sidebar state from localStorage or defaults to 'expanded'.
 */
export function applySidebarState() {
    if (!sidebar) return;

    const savedState = localStorage.getItem(SIDEBAR_STATE_KEY) || 'expanded';
    sidebar.className = savedState;
    updateSidebarIcon(savedState);
}

/**
 * Toggles the sidebar state between 'expanded' and 'collapsed'.
 */
export function toggleSidebar() {
    if (!sidebar) return;

    const isExpanded = sidebar.classList.contains('expanded');
    const newState = isExpanded ? 'collapsed' : 'expanded';
    sidebar.className = newState;
    localStorage.setItem(SIDEBAR_STATE_KEY, newState);
    updateSidebarIcon(newState);

    // Handle overlay for mobile
    if (window.innerWidth <= 768) {
        if (newState === 'expanded') {
            sidebarOverlay.style.visibility = 'visible';
            sidebarOverlay.style.opacity = '1';
            sidebarOverlay.style.transition = 'opacity var(--transition-med)';
        } else {
            sidebarOverlay.style.opacity = '0';
            sidebarOverlay.style.transition = 'opacity var(--transition-med), visibility 0s var(--transition-med)';
            sidebarOverlay.style.visibility = 'hidden';
        }
    }
}

function updateSidebarIcon(state) {
    if (!sidebarToggleButton) return;
    const collapseIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>`;
    const expandIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>`;
    sidebarToggleButton.innerHTML = state === 'expanded' ? collapseIcon : expandIcon;
}

// Add event listener for the overlay
if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
        if (sidebar.classList.contains('expanded')) {
            toggleSidebar();
        }
    });
}


/**
 * Populates the agent selection dropdown.
 * @param {string[]} agentNames - An array of agent names.
 */
export function populateAgentSelector(agentNames) {
    agentSelect.innerHTML = ''; // Clear loading text
    agentNames.forEach(agentName => {
        const option = document.createElement('option');
        option.value = agentName;
        option.textContent = agentName;
        agentSelect.appendChild(option);
    });
    // Enable the form now that agents are loaded
    promptInput.disabled = false;
    sendButton.disabled = promptInput.value.trim() === '';
}

/**
 * Populates the mode selection dropdown based on the selected agent's capabilities.
 * @param {object} modes - An object where keys are mode IDs and values are mode details.
 */
export function populateModeSelector(modes) {
    const modeSelect = document.getElementById('mode-select');
    modeSelect.innerHTML = '<option value="">Default</option>'; // Reset with default

    if (modes && Object.keys(modes).length > 0) {
        for (const modeId in modes) {
            const option = document.createElement('option');
            option.value = modeId;
            option.textContent = modes[modeId].name || modeId; // Use name if available, else ID
            modeSelect.appendChild(option);
        }
        modeSelect.disabled = false;
    } else {
        modeSelect.disabled = true;
    }
}

/**
 * Handles errors during agent loading.
 */
export function handleAgentError() {
    agentSelect.innerHTML = '<option>Error loading agents</option>';
}

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
    chatWindow.appendChild(messageDiv);
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