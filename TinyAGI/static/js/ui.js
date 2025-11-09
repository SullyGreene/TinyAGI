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
const musicStudioModal = document.getElementById('music-studio-modal');
const videoStudioModal = document.getElementById('video-studio-modal');
const temperatureSlider = document.getElementById('temperature-slider');
const temperatureValue = document.getElementById('temperature-value');
const maxTokensSlider = document.getElementById('max-tokens-slider');
const maxTokensValue = document.getElementById('max-tokens-value');
const systemPromptTextarea = document.getElementById('system-prompt');
const themeToggleButton = document.getElementById('theme-toggle-button');

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
 * Populates the agent management list.
 * @param {string[]} agentNames - An array of agent names.
 * @param {string} activeAgentName - The name of the currently selected agent.
 */
export function populateAgentManagerList(agentNames, activeAgentName) {
    const container = document.getElementById('agent-list-container');
    if (!container) return;
    container.innerHTML = ''; // Clear previous list

    agentNames.forEach(agentName => {
        const agentItem = document.createElement('div');
        agentItem.className = 'agent-item';
        if (agentName === activeAgentName) {
            agentItem.classList.add('active');
        }
        agentItem.dataset.agentName = agentName;

        const agentNameSpan = document.createElement('span');
        agentNameSpan.textContent = agentName;
        agentNameSpan.className = 'agent-name-selectable'; // Class to handle selection clicks

        const agentActions = document.createElement('div');
        agentActions.className = 'agent-item-actions';

        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.className = 'button-secondary agent-edit-button';
        editButton.dataset.agentName = agentName;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'button-danger agent-delete-button';
        deleteButton.dataset.agentName = agentName;

        agentActions.appendChild(editButton);
        agentActions.appendChild(deleteButton);

        agentItem.appendChild(agentNameSpan);
        agentItem.appendChild(agentActions);
        container.appendChild(agentItem);
    });
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
    } else {
        // For assistant, we can put a placeholder or leave it empty,
        // as it will be populated by the streaming update function.
        contentDiv.innerHTML = content;
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
    sendButton.style.display = isGenerating ? 'none' : 'flex';
    stopButton.style.display = isGenerating ? 'flex' : 'none';
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
 * Opens or closes the agent management modal.
 * @param {boolean} show - True to show the modal, false to hide it.
 */
export function toggleAgentModal(show) {
    if (agentModal) {
        agentModal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Opens or closes the edit agent modal.
 * @param {boolean} show - True to show the modal, false to hide it.
 */
export function toggleEditAgentModal(show) {
    if (editAgentModal) {
        editAgentModal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Populates the edit agent form with the agent's details.
 * @param {object} agentDetails - The agent's configuration object.
 */
export function populateEditAgentForm(agentDetails) {
    const nameTitle = document.getElementById('edit-agent-name-title');
    const originalNameInput = document.getElementById('edit-agent-original-name');
    const descriptionInput = document.getElementById('edit-agent-description');
    const modelInput = document.getElementById('edit-agent-model');
    const systemPromptTextarea = document.getElementById('edit-agent-system-prompt');

    if (nameTitle) nameTitle.textContent = agentDetails.name;
    if (originalNameInput) originalNameInput.value = agentDetails.name;

    // Use empty string as fallback for optional fields
    if (descriptionInput) descriptionInput.value = agentDetails.description || '';
    if (systemPromptTextarea) systemPromptTextarea.value = agentDetails.system_prompt || '';

    // The 'model' can be in different places depending on the agent type
    let modelName = '';
    if (agentDetails.model) modelName = agentDetails.model;
    else if (agentDetails.config && agentDetails.config.generation_model) modelName = agentDetails.config.generation_model;
    if (modelInput) modelInput.value = modelName;
}

/**
 * Opens or closes the create agent modal.
 * @param {boolean} show - True to show the modal, false to hide it.
 */
export function toggleCreateAgentModal(show) {
    if (createAgentModal) {
        createAgentModal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Opens or closes the image studio modal.
 * @param {boolean} show - True to show the modal, false to hide it.
 */
export function toggleImageStudioModal(show) {
    if (imageStudioModal) {
        imageStudioModal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Opens or closes the music studio modal.
 * @param {boolean} show - True to show the modal, false to hide it.
 */
export function toggleMusicStudioModal(show) {
    if (musicStudioModal) {
        musicStudioModal.style.display = show ? 'flex' : 'none';
    }
}
/**
 * Opens or closes the video studio modal.
 * @param {boolean} show - True to show the modal, false to hide it.
 */
export function toggleVideoStudioModal(show) {
    if (videoStudioModal) {
        videoStudioModal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Populates the image agent selection dropdown.
 * @param {string[]} agentNames - An array of image-capable agent names.
 */
export function populateImageAgentSelector(agentNames) {
    const imageAgentSelect = document.getElementById('image-agent-select');
    if (!imageAgentSelect) return;

    imageAgentSelect.innerHTML = '';
    if (agentNames.length === 0) {
        imageAgentSelect.innerHTML = '<option>No image agents found</option>';
        imageAgentSelect.disabled = true;
    } else {
        agentNames.forEach(agentName => {
            const option = document.createElement('option');
            option.value = agentName;
            option.textContent = agentName;
            imageAgentSelect.appendChild(option);
        });
        imageAgentSelect.disabled = false;
    }
}

/**
 * Displays a spinner in the image results panel.
 * @param {HTMLElement} panel - The panel to display the spinner in.
 */
export function showImageGenerationSpinner(panel) {
    panel.innerHTML = `<div class="typing-indicator" style="margin: auto;"><span></span><span></span><span></span></div>`;
}

/**
 * Displays the generated images in the results panel.
 * @param {HTMLElement} panel - The panel to display images in.
 * @param {string[]} imagesBase64 - An array of base64 encoded image strings.
 */
export function displayGeneratedImages(panel, imagesBase64) {
    panel.innerHTML = '';
    imagesBase64.forEach(base64String => {
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${base64String}`;
        img.style.width = '100%';
        img.style.height = 'auto';
        img.style.borderRadius = '8px';
        panel.appendChild(img);
    });
}

/**
 * Populates the video agent selection dropdown.
 * @param {string[]} agentNames - An array of video-capable agent names.
 */
export function populateVideoAgentSelector(agentNames) {
    const videoAgentSelect = document.getElementById('video-agent-select');
    if (!videoAgentSelect) return;

    videoAgentSelect.innerHTML = '';
    if (agentNames.length === 0) {
        videoAgentSelect.innerHTML = '<option>No video agents found</option>';
        videoAgentSelect.disabled = true;
    } else {
        agentNames.forEach(agentName => {
            const option = document.createElement('option');
            option.value = agentName;
            option.textContent = agentName;
            videoAgentSelect.appendChild(option);
        });
        videoAgentSelect.disabled = false;
    }
}

/**
 * Displays a spinner in the video result container.
 * @param {HTMLElement} container - The container to display the spinner in.
 */
export function showVideoGenerationSpinner(container) {
    container.innerHTML = `<div style="text-align: center; padding: 2rem;">
        <div class="typing-indicator" style="margin: auto;"><span></span><span></span><span></span></div>
        <p style="margin-top: 1rem; color: var(--text-secondary);">Generating video... This may take several minutes.</p>
    </div>`;
}

/**
 * Displays the generated video in the result container.
 * @param {HTMLElement} container - The container to display the video in.
 * @param {string} videoUrl - The URL of the generated video.
 */
export function displayVideoResult(container, videoUrl) {
    container.innerHTML = `<video controls autoplay loop style="width: 100%; border-radius: 8px;">
        <source src="${videoUrl}" type="video/mp4">
        Your browser does not support the video tag.
    </video>`;
}

/**
 * Updates the status message in the music studio.
 * @param {string} text - The message to display.
 * @param {boolean} isError - Whether the message is an error.
 */
export function updateMusicStatus(text, isError = false) {
    const statusEl = document.getElementById('music-status');
    if (statusEl) {
        statusEl.textContent = text;
        statusEl.style.color = isError ? 'var(--accent-danger)' : 'var(--text-secondary)';
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
    if (maxTokensSlider) maxTokensSlider.value = value;
}

/**
 * Sets the value of the system prompt textarea.
 * @param {string} text - The text to set.
 */
export function setSystemPrompt(text) {
    if (systemPromptTextarea) systemPromptTextarea.value = text;
}