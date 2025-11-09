import { fetchAgents, streamChat } from './api.js';
import {
    populateAgentSelector,
    handleAgentError,
    addMessage,
    showThinkingIndicator,
    updateAssistantMessage,
    setFormDisabled,
    clearChatWindow,
    toggleStopButton,
    toggleSettingsModal,
    updateTemperatureDisplay,
    setTemperatureValue,
    updateMaxTokensDisplay,
    setMaxTokensValue,
    setSystemPrompt
} from './ui.js';

const agentSelect = document.getElementById('agent-select');
const chatWindow = document.getElementById('chat-window');
const promptInput = document.getElementById('prompt-input');
const sendButton = document.getElementById('send-button');
const clearChatButton = document.getElementById('clear-chat-button');
const stopButton = document.getElementById('stop-button');
const settingsButton = document.getElementById('settings-button');
const closeModalButton = document.getElementById('close-modal-button');
const saveSettingsButton = document.getElementById('save-settings-button');
const temperatureSlider = document.getElementById('temperature-slider');
const maxTokensSlider = document.getElementById('max-tokens-slider');
const systemPromptTextarea = document.getElementById('system-prompt');

const SETTINGS_KEY = 'tinyagi_settings';

let messages = [];
let abortController = null;
let settings = {
    temperature: 1.0,
    max_tokens: 4096,
    system_prompt: ''
};



async function loadAgents() {
    try {
        const agents = await fetchAgents();
        populateAgentSelector(agents);
    } catch (error) {
        console.error("Could not load agents:", error);
        handleAgentError();
    }
}

async function handleSend() {
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    const selectedAgent = agentSelect.value;
    if (!selectedAgent || selectedAgent === 'Error loading agents') {
        alert('Please select a valid agent.');
        return;
    }

    addMessage('user', prompt);
    messages.push({ role: 'user', content: prompt });
    promptInput.value = '';
    setFormDisabled(true);
    toggleStopButton(true);

    const assistantContentDiv = showThinkingIndicator();
    let assistantResponse = '';

    abortController = new AbortController();

    // Prepare messages for the API call, including the system prompt
    const systemPrompt = systemPromptTextarea.value.trim();
    const messagesToSend = [...messages];
    if (systemPrompt) {
        messagesToSend.unshift({ role: 'system', content: systemPrompt });
    }

    try {
        const stream = await streamChat(selectedAgent, messagesToSend, settings, abortController.signal);
        const reader = stream.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            assistantResponse += chunk;
            updateAssistantMessage(assistantContentDiv, assistantResponse);
        }
        messages.push({ role: 'assistant', content: assistantResponse });
    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Stream generation stopped by user.');
            updateAssistantMessage(assistantContentDiv, assistantResponse + ' [Stopped]');
            messages.push({ role: 'assistant', content: assistantResponse + ' [Stopped]'});
        } else {
            console.error('Error sending message:', error);
            updateAssistantMessage(assistantContentDiv, `Sorry, an error occurred: ${error.message}`);
        }
    } finally {
        setFormDisabled(false);
        toggleStopButton(false);
        promptInput.focus();
        abortController = null;
    }
}

function handleClearChat() {
    // Clear the in-memory message history
    messages = [];
    // Clear the messages from the UI
    clearChatWindow();
    // Add a welcome message or leave it blank
    // addMessage('assistant', 'Chat cleared. How can I help you?');
    console.log('Chat history cleared.');
}

function handleStop() {
    if (abortController) {
        abortController.abort();
        console.log('Abort button clicked. Cancelling stream...');
    }
}

function handleCopyClick(event) {
    if (!event.target.classList.contains('copy-button')) return;

    const button = event.target;
    const pre = button.closest('pre');
    if (!pre) return;

    const code = pre.querySelector('code');
    if (!code) return;

    navigator.clipboard.writeText(code.innerText).then(() => {
        button.textContent = 'Copied!';
        button.style.backgroundColor = '#28a745'; // Green color for success
        setTimeout(() => {
            button.textContent = 'Copy';
            button.style.backgroundColor = ''; // Revert to original color
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

function loadSettings() {
    const savedSettings = localStorage.getItem(SETTINGS_KEY);
    if (savedSettings) {
        try {
            const parsedSettings = JSON.parse(savedSettings);
            // Merge with defaults to handle new settings added in future versions
            settings = { ...settings, ...parsedSettings };
            console.log('Loaded settings from localStorage:', settings);
        } catch (e) {
            console.error('Failed to parse settings from localStorage:', e);
        }
    }
}

function saveSettings() {
    try {
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
        console.log('Settings saved to localStorage:', settings);
    } catch (e) {
        console.error('Failed to save settings to localStorage:', e);
    }
}

function handleSaveSettings() {
    settings.temperature = parseFloat(temperatureSlider.value);
    settings.max_tokens = parseInt(maxTokensSlider.value, 10);
    // System prompt is saved on input, but we could re-save all here if needed.
    saveSettings();
    toggleSettingsModal(false);
}

function initialize() {
    loadSettings(); // Load settings on startup

    // Set initial values in the UI from loaded settings
    setTemperatureValue(settings.temperature);
    setMaxTokensValue(settings.max_tokens);
    setSystemPrompt(settings.system_prompt);

    sendButton.addEventListener('click', handleSend);
    clearChatButton.addEventListener('click', handleClearChat);
    stopButton.addEventListener('click', handleStop);
    settingsButton.addEventListener('click', () => toggleSettingsModal(true));
    closeModalButton.addEventListener('click', () => toggleSettingsModal(false));
    saveSettingsButton.addEventListener('click', handleSaveSettings);
    temperatureSlider.addEventListener('input', updateTemperatureDisplay);
    maxTokensSlider.addEventListener('input', updateMaxTokensDisplay);
    systemPromptTextarea.addEventListener('input', () => {
        settings.system_prompt = systemPromptTextarea.value;
        saveSettings();
    });

    promptInput.addEventListener('keypress', (e) => e.key === 'Enter' && handleSend());
    promptInput.addEventListener('input', () => {
        // Only enable send if not currently streaming a response
        if (!promptInput.disabled) {
            sendButton.disabled = promptInput.value.trim() === '';
        }
    });

    // Add a single event listener to the chat window for copy buttons
    chatWindow.addEventListener('click', handleCopyClick);

    loadAgents();
}

initialize();