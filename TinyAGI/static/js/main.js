import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import { fetchAgents, streamChat, deleteAgent, fetchAgentDetails, updateAgent, createAgent } from './api.js';
import {
    populateAgentSelector,
    handleAgentError,
    addMessage,
    showThinkingIndicator,
    updateAssistantMessage,
    setFormDisabled,
    clearChatWindow,
    populateAgentManagerList,
    toggleStopButton,
    toggleSettingsModal,
    toggleEditAgentModal,
    toggleCreateAgentModal,
    populateEditAgentForm,
    toggleAgentModal,
    updateTemperatureDisplay,
    setTemperatureValue,
    updateMaxTokensDisplay,
    setMaxTokensValue,
    setSystemPrompt,
    toggleTheme,
    applyTheme
} from './ui.js';

const agentSelect = document.getElementById('agent-select');
const chatWindow = document.getElementById('chat-window');
const promptInput = document.getElementById('prompt-input'); // This is now a textarea
const sendButton = document.getElementById('send-button');
const clearChatButton = document.getElementById('new-chat-button'); // Renamed from 'clear-chat-button'
const stopButton = document.getElementById('stop-button');
const agentListContainer = document.getElementById('agent-list-container');
const manageAgentsButton = document.getElementById('manage-agents-button');
const settingsButton = document.getElementById('settings-button');
const createAgentButton = document.getElementById('create-agent-button');
const confirmCreateAgentButton = document.getElementById('confirm-create-agent-button');
const closeEditAgentModalButton = document.querySelector('#edit-agent-modal .close-button');
const closeAgentModalButton = document.querySelector('#agent-modal .close-button');
const closeModalButton = document.querySelector('.modal .close-button');
const closeCreateAgentModalButton = document.querySelector('#create-agent-modal .close-button');
const saveAgentButton = document.getElementById('save-agent-button');
const themeToggleButton = document.getElementById('theme-toggle-button');

const saveSettingsButton = document.getElementById('save-settings-button');
const temperatureSlider = document.getElementById('temperature-slider');
const maxTokensSlider = document.getElementById('max-tokens-slider');

const systemPromptTextarea = document.getElementById('system-prompt');

const SETTINGS_KEY = 'tinyagi_chat_settings';

let messages = [];
let agentsList = []; // To store the list of agents
let abortController = null; // To cancel fetch requests
let settings = {
    temperature: 1.0,
    max_tokens: 4096,
    system_prompt: ''
};


// --- Utility Functions ---

function adjustTextareaHeight(textarea) {
    textarea.style.height = 'auto'; // Reset height
    textarea.style.height = `${textarea.scrollHeight}px`; // Set to scroll height
}

async function loadAgents() {
    try {
        agentsList = await fetchAgents();
        populateAgentSelector(agentsList);
        populateAgentManagerList(agentsList, agentSelect.value);
    } catch (error) {
        console.error("Could not load agents:", error);
        handleAgentError();
    }
}

// --- Core Chat Logic ---

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
    adjustTextareaHeight(promptInput); // Reset textarea height
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
            updateAssistantMessage(assistantContentDiv, marked.parse(assistantResponse));
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

// --- Event Handlers ---

function handleClearChat() {
    messages = [];
    clearChatWindow();
    addMessage('assistant', 'New chat started. How can I help you?');
    console.log('Chat history cleared.');
}

function handleStop() {
    if (abortController) {
        abortController.abort();
        console.log('Abort button clicked. Cancelling stream...');
    }
}

// Handle clicks on dynamically added copy buttons
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

function handleAgentSelection(event) {
    const target = event.target;

    // Handle clicks on the "Delete" button
    if (target.classList.contains('agent-delete-button')) {
        handleDeleteAgent(target.dataset.agentName);
        return;
    }

    // Handle clicks on the "Edit" button
    if (target.classList.contains('agent-edit-button')) {
        handleEditAgent(target.dataset.agentName);
        return;
    }

    // Handle clicks on the agent name for selection
    const selectableArea = target.closest('.agent-name-selectable');
    if (!selectableArea) return;

    const agentItem = selectableArea.closest('.agent-item');

    const agentName = agentItem.dataset.agentName;
    if (agentName) {
        // Set the main agent selector
        agentSelect.value = agentName;

        // Update the active state in the modal list
        populateAgentManagerList(agentsList, agentName);

        // Close the modal
        toggleAgentModal(false);
    }
}

async function handleDeleteAgent(agentName) {
    if (!confirm(`Are you sure you want to delete the agent "${agentName}"? This cannot be undone.`)) {
        return;
    }
    try {
        const result = await deleteAgent(agentName);
        alert(result.message); // Show success message
        await loadAgents(); // Reload agent lists
    } catch (error) {
        console.error(`Failed to delete agent ${agentName}:`, error);
        alert(`Error: ${error.message}`);
    }
}

async function handleEditAgent(agentName) {
    try {
        const agentDetails = await fetchAgentDetails(agentName);
        populateEditAgentForm(agentDetails);
        toggleEditAgentModal(true);
    } catch (error) {
        console.error(`Failed to fetch details for agent ${agentName}:`, error);
        alert(`Error: ${error.message}`);
    }
}

async function handleSaveAgent() {
    const originalName = document.getElementById('edit-agent-original-name').value;
    const description = document.getElementById('edit-agent-description').value;
    const model = document.getElementById('edit-agent-model').value;
    const system_prompt = document.getElementById('edit-agent-system-prompt').value;

    const updateData = {
        description,
        model, // The backend will know where to place this
        system_prompt,
    };

    try {
        const result = await updateAgent(originalName, updateData);
        alert(result.message);
        toggleEditAgentModal(false);
        await loadAgents(); // Reload agent lists to reflect changes
    } catch (error) {
        console.error(`Failed to update agent ${originalName}:`, error);
        alert(`Error: ${error.message}`);
    }
}

async function handleCreateAgent() {
    const name = document.getElementById('create-agent-name').value.trim();
    const type = document.getElementById('create-agent-type').value;
    const description = document.getElementById('create-agent-description').value;
    const model = document.getElementById('create-agent-model').value;
    const system_prompt = document.getElementById('create-agent-system-prompt').value;

    if (!name) {
        alert('Agent Name is required.');
        return;
    }

    try {
        const result = await createAgent({ name, type, description, model, system_prompt });
        alert(result.message);
        toggleCreateAgentModal(false);
        await loadAgents(); // Reload agent lists
    } catch (error) {
        console.error(`Failed to create agent:`, error);
        alert(`Error: ${error.message}`);
    }
}

// --- Settings Management ---

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
    settings.system_prompt = systemPromptTextarea.value;
    saveSettings();
    toggleSettingsModal(false);
}

// --- Initialization ---

function initialize() {
    applyTheme(); // Apply saved theme on startup
    loadSettings(); // Load settings on startup

    // Set initial values in the UI from loaded settings
    setTemperatureValue(settings.temperature);
    updateTemperatureDisplay(); // Also update the label
    setMaxTokensValue(settings.max_tokens);
    updateMaxTokensDisplay(); // Also update the label
    setSystemPrompt(settings.system_prompt);

    sendButton.addEventListener('click', handleSend);
    clearChatButton.addEventListener('click', handleClearChat);
    stopButton.addEventListener('click', handleStop);
    settingsButton.addEventListener('click', () => toggleSettingsModal(true));
    manageAgentsButton.addEventListener('click', () => {
        populateAgentManagerList(agentsList, agentSelect.value);
        toggleAgentModal(true);
    });
    themeToggleButton.addEventListener('click', toggleTheme);
    createAgentButton.addEventListener('click', () => toggleCreateAgentModal(true));
    confirmCreateAgentButton.addEventListener('click', handleCreateAgent);
    closeEditAgentModalButton.addEventListener('click', () => toggleEditAgentModal(false));
    closeAgentModalButton.addEventListener('click', () => toggleAgentModal(false));
    closeModalButton.addEventListener('click', () => toggleSettingsModal(false));
    saveAgentButton.addEventListener('click', handleSaveAgent);
    closeCreateAgentModalButton.addEventListener('click', () => toggleCreateAgentModal(false));
    saveSettingsButton.addEventListener('click', handleSaveSettings);
    temperatureSlider.addEventListener('input', updateTemperatureDisplay);
    maxTokensSlider.addEventListener('input', updateMaxTokensDisplay);
    // System prompt is now saved only when the "Save" button is clicked.

    promptInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevent new line on Enter
            handleSend();
        }
    });
    promptInput.addEventListener('input', () => {
        adjustTextareaHeight(promptInput);
        if (!promptInput.disabled) {
            sendButton.disabled = promptInput.value.trim() === '';
        }
    });
    
    // Add a single event listener to the chat window for copy buttons
    chatWindow.addEventListener('click', handleCopyClick);

    // Add event listener for agent selection in the modal
    agentListContainer.addEventListener('click', handleAgentSelection);

    loadAgents();
}

initialize();
addMessage('assistant', 'Welcome to TinyAGI! Select an agent and start chatting.');