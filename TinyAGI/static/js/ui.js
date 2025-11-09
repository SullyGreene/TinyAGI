const agentSelect = document.getElementById('agent-select');
const chatWindow = document.getElementById('chat-window');
const promptInput = document.getElementById('prompt-input');
const sendButton = document.getElementById('send-button');
const stopButton = document.getElementById('stop-button');
const settingsModal = document.getElementById('settings-modal');
const temperatureSlider = document.getElementById('temperature-slider');
const temperatureValue = document.getElementById('temperature-value');
const maxTokensSlider = document.getElementById('max-tokens-slider');
const maxTokensValue = document.getElementById('max-tokens-value');


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
export function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';
    // For user messages, we just set text content to avoid any HTML injection.
    // For assistant messages, we will parse markdown.
    if (role === 'user') {
        contentDiv.textContent = content;
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
 * @param {string} fullResponse - The full response text to display.
 */
export function updateAssistantMessage(contentDiv, fullResponse) {
    // Remove thinking style on first update
    if (contentDiv.classList.contains('thinking')) {
        contentDiv.classList.remove('thinking');
        contentDiv.textContent = ''; // Clear "thinking..." text
    }
    // WARNING: Using innerHTML can be risky if the source is not trusted.
    // Since we control the AI, we accept this risk for rich formatting.
    // For production apps with external sources, use a sanitizer like DOMPurify.
    contentDiv.innerHTML = marked.parse(fullResponse);
    chatWindow.scrollTop = chatWindow.scrollHeight;

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
        if (codeBlock) {
            hljs.highlightElement(codeBlock);
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
    chatWindow.innerHTML = '';
}

/**
 * Toggles between the Send and Stop buttons.
 * @param {boolean} isGenerating - True if the AI is generating a response.
 */
export function toggleStopButton(isGenerating) {
    const inputArea = document.getElementById('input-area');
    sendButton.style.display = isGenerating ? 'none' : 'flex';
    stopButton.style.display = isGenerating ? 'flex' : 'none';
    // Hide the text input when the stop button is visible
    promptInput.style.display = isGenerating ? 'none' : 'flex';
}

/**
 * Opens or closes the settings modal.
 * @param {boolean} show - True to show the modal, false to hide it.
 */
export function toggleSettingsModal(show) {
    if (settingsModal) {
        settingsModal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Updates the displayed value for the temperature slider.
 */
export function updateTemperatureDisplay() {
    if (temperatureValue && temperatureSlider) {
        temperatureValue.textContent = parseFloat(temperatureSlider.value).toFixed(1);
    }
}

/**
 * Sets the value of the temperature slider.
 * @param {number} value - The value to set.
 */
export function setTemperatureValue(value) {
    if (temperatureSlider) temperatureSlider.value = value;
    updateTemperatureDisplay();
}

/**
 * Updates the displayed value for the max tokens slider.
 */
export function updateMaxTokensDisplay() {
    if (maxTokensValue && maxTokensSlider) {
        maxTokensValue.textContent = maxTokensSlider.value;
    }
}

/**
 * Sets the value of the max tokens slider.
 * @param {number} value - The value to set.
 */
export function setMaxTokensValue(value) {
    if (maxTokensSlider) {
        maxTokensSlider.value = value;
    }
    updateMaxTokensDisplay();
}