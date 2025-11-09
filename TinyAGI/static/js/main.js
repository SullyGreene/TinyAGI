import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import { fetchAgents, streamChat, deleteAgent, fetchAgentDetails, updateAgent, createAgent, generateImages, startVideoGeneration, pollVideoOperation, processRoboticsImage } from './api.js';
import {
    populateModeSelector,
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
    toggleRoboticsStudioModal,
    toggleMusicStudioModal,
    toggleVideoStudioModal,
    toggleImageStudioModal,
    populateEditAgentForm,
    toggleAgentModal,
    updateTemperatureDisplay,
    setTemperatureValue,
    updateMaxTokensDisplay,
    setMaxTokensValue,
    setSystemPrompt,
    populateImageAgentSelector,
    displayGeneratedImages,
    populateVideoAgentSelector,
    populateRoboticsAgentSelector,
    displayRoboticsResult,
    showRoboticsSpinner,
    updateMusicStatus,
    displayVideoResult,
    showVideoGenerationSpinner,
    showImageGenerationSpinner,
    toggleTheme,
    applyTheme
} from './ui.js';

const agentSelect = document.getElementById('agent-select');
const modeSelect = document.getElementById('mode-select');
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
const closeImageStudioModalButton = document.querySelector('#image-studio-modal .close-button');
const closeRoboticsStudioModalButton = document.querySelector('#robotics-studio-modal .close-button');
const closeMusicStudioModalButton = document.querySelector('#music-studio-modal .close-button');
const closeVideoStudioModalButton = document.querySelector('#video-studio-modal .close-button');
const saveAgentButton = document.getElementById('save-agent-button');
const themeToggleButton = document.getElementById('theme-toggle-button');
const createAgentTypeSelect = document.getElementById('create-agent-type');

const saveSettingsButton = document.getElementById('save-settings-button');
const temperatureSlider = document.getElementById('temperature-slider');
const maxTokensSlider = document.getElementById('max-tokens-slider');

const imageStudioButton = document.getElementById('image-studio-button');
const generateImageButton = document.getElementById('generate-image-button');
const imageAgentSelect = document.getElementById('image-agent-select');
const imagePrompt = document.getElementById('image-prompt');
const imageCountSlider = document.getElementById('image-count-slider');
const imageAspectRatioSelect = document.getElementById('image-aspect-ratio');

const videoStudioButton = document.getElementById('video-studio-button');
const generateVideoButton = document.getElementById('generate-video-button');
const videoAgentSelect = document.getElementById('video-agent-select');
const videoPrompt = document.getElementById('video-prompt');
const videoDurationSelect = document.getElementById('video-duration-select');

const musicStudioButton = document.getElementById('music-studio-button');
const startMusicButton = document.getElementById('start-music-button');
const steerMusicButton = document.getElementById('steer-music-button');
const stopMusicButton = document.getElementById('stop-music-button');
const musicPromptInput = document.getElementById('music-prompt');
const musicSteerPromptInput = document.getElementById('music-steer-prompt');
const systemPromptTextarea = document.getElementById('system-prompt');

const roboticsStudioButton = document.getElementById('robotics-studio-button');
const processRoboticsImageButton = document.getElementById('process-robotics-image-button');
const roboticsAgentSelect = document.getElementById('robotics-agent-select');
const roboticsImageUpload = document.getElementById('robotics-image-upload');
const roboticsPrompt = document.getElementById('robotics-prompt');

const SETTINGS_KEY = 'tinyagi_chat_settings';

let messages = [];
let agentsList = []; // To store the list of agents
let abortController = null; // To cancel fetch requests

let musicSocket = null;
let audioContext = null;
let audioQueue = [];
let isPlayingMusic = false;
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

async function handleAgentChange(agentName) {
    try {
        const agentDetails = await fetchAgentDetails(agentName);
        const modes = agentDetails.modes || {};
        populateModeSelector(modes);
    } catch (error) {
        console.error(`Could not load modes for agent ${agentName}:`, error);
        populateModeSelector({}); // Clear the modes dropdown on error
    }
}

// --- Core Chat Logic ---

async function handleSend() {
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    const selectedAgent = agentSelect.value;
    const selectedMode = modeSelect.value;
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
        const stream = await streamChat(selectedAgent, messagesToSend, settings, selectedMode, abortController.signal);
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

        // Trigger update of modes for the newly selected agent
        handleAgentChange(agentName);
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
    // Handle both input and select for model name
    const modelInput = document.getElementById('create-agent-model-input') || document.getElementById('create-agent-model-select');
    const model = modelInput.value;
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

function handleCreateAgentTypeChange() {
    const agentType = createAgentTypeSelect.value;
    const modelContainer = document.getElementById('create-agent-model-container');
    
    const geminiModels = [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite"
    ];

    if (agentType === 'gemini') {
        // Create a select dropdown for Gemini models
        let selectHTML = '<select id="create-agent-model-select">';
        geminiModels.forEach(model => {
            selectHTML += `<option value="${model}">${model}</option>`;
        });
        selectHTML += '</select>';
        modelContainer.innerHTML = selectHTML;
    } else {
        // Revert to a text input for other types
        let placeholder = 'e.g., llama3, gemma:2b';
        let defaultValue = 'llama3';
        if (agentType === 'huggingface') {
            placeholder = 'e.g., distilgpt2';
            defaultValue = 'distilgpt2';
        }
        modelContainer.innerHTML = `<input type="text" id="create-agent-model-input" value="${defaultValue}" placeholder="${placeholder}">`;
    }
}

function resetCreateAgentForm() {
    document.getElementById('create-agent-name').value = '';
    document.getElementById('create-agent-description').value = '';
    document.getElementById('create-agent-system-prompt').value = '';
    handleCreateAgentTypeChange(); // Reset model input based on default type
}
// --- Settings Management ---

// --- Image Generation ---

async function handleGenerateImages() {
    const agent = imageAgentSelect.value;
    const prompt = imagePrompt.value.trim();
    const settings = {
        number_of_images: parseInt(imageCountSlider.value, 10),
        aspect_ratio: imageAspectRatioSelect.value
    };

    if (!prompt) {
        alert('Please enter a prompt.');
        return;
    }

    const resultsPanel = document.getElementById('image-results-panel');
    showImageGenerationSpinner(resultsPanel);
    generateImageButton.disabled = true;

    try {
        const result = await generateImages(agent, prompt, settings);
        displayGeneratedImages(resultsPanel, result.images);
    } catch (error) {
        alert(`Error generating images: ${error.message}`);
        resultsPanel.innerHTML = `<p style="color: var(--accent-danger);">Failed to generate images. Please check the console for details.</p>`;
    } finally {
        generateImageButton.disabled = false;
    }
}

// --- Video Generation ---

async function handleGenerateVideo() {
    const agent = videoAgentSelect.value;
    const prompt = videoPrompt.value.trim();
    const settings = {
        duration_seconds: videoDurationSelect.value
    };

    if (!prompt) {
        alert('Please enter a prompt for the video.');
        return;
    }

    const resultContainer = document.getElementById('video-result-container');
    showVideoGenerationSpinner(resultContainer);
    generateVideoButton.disabled = true;

    try {
        const startResponse = await startVideoGeneration(agent, prompt, settings);
        const operationName = startResponse.operation_name;

        // Start polling
        const pollInterval = setInterval(async () => {
            const statusResponse = await pollVideoOperation(operationName);
            if (statusResponse.status === 'complete') {
                clearInterval(pollInterval);
                displayVideoResult(resultContainer, statusResponse.url);
                generateVideoButton.disabled = false;
            } else if (statusResponse.status === 'failed') {
                clearInterval(pollInterval);
                alert(`Video generation failed: ${statusResponse.error}`);
                resultContainer.innerHTML = `<p style="color: var(--accent-danger);">Video generation failed.</p>`;
                generateVideoButton.disabled = false;
            }
            // If status is 'processing', do nothing and wait for the next poll.
        }, 10000); // Poll every 10 seconds
    } catch (error) {
        alert(`Error starting video generation: ${error.message}`);
        resultContainer.innerHTML = `<p style="color: var(--accent-danger);">Could not start video generation.</p>`;
        generateVideoButton.disabled = false;
    }
}

// --- Music Generation ---

function setupMusicSocket() {
    if (musicSocket) return;

    musicSocket = io('/music');

    musicSocket.on('connect', () => {
        console.log('Connected to music server.');
    });

    musicSocket.on('stream_started', () => {
        updateMusicStatus('Streaming...');
        startMusicButton.disabled = true;
        steerMusicButton.disabled = false;
        stopMusicButton.disabled = false;
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 48000 });
        }
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }
        isPlayingMusic = true;
        playAudioQueue();
    });

    musicSocket.on('audio_chunk', (chunk) => {
        // The chunk is ArrayBuffer-like, convert it to a Float32Array
        const int16Array = new Int16Array(chunk);
        const float32Array = new Float32Array(int16Array.length);
        for (let i = 0; i < int16Array.length; i++) {
            float32Array[i] = int16Array[i] / 32768.0; // Convert 16-bit PCM to float
        }
        audioQueue.push(float32Array);
    });

    musicSocket.on('stream_error', (data) => {
        updateMusicStatus(`Error: ${data.error}`, true);
        stopMusicStream();
    });
}

function playAudioQueue() {
    if (!isPlayingMusic || audioQueue.length === 0) return;

    const audioData = audioQueue.shift();
    const audioBuffer = audioContext.createBuffer(2, audioData.length / 2, audioContext.sampleRate);
    audioBuffer.copyToChannel(audioData.filter((_, i) => i % 2 === 0), 0); // Left channel
    audioBuffer.copyToChannel(audioData.filter((_, i) => i % 2 !== 0), 1); // Right channel

    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
    source.onended = playAudioQueue; // Play next chunk when this one finishes
}

function stopMusicStream() {
    if (musicSocket) {
        musicSocket.disconnect();
        musicSocket = null;
    }
    isPlayingMusic = false;
    audioQueue = [];
    updateMusicStatus('Ready to generate music.');
    startMusicButton.disabled = false;
    steerMusicButton.disabled = true;
    stopMusicButton.disabled = true;
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
    agentSelect.addEventListener('change', (e) => handleAgentChange(e.target.value));
    clearChatButton.addEventListener('click', handleClearChat);
    stopButton.addEventListener('click', handleStop);
    settingsButton.addEventListener('click', () => toggleSettingsModal(true));
    manageAgentsButton.addEventListener('click', () => {
        populateAgentManagerList(agentsList, agentSelect.value);
        toggleAgentModal(true);
    });
    createAgentTypeSelect.addEventListener('change', handleCreateAgentTypeChange);
    createAgentButton.addEventListener('click', () => {
        resetCreateAgentForm();
        toggleCreateAgentModal(true);
    });
    createAgentButton.addEventListener('click', () => toggleCreateAgentModal(true));
    confirmCreateAgentButton.addEventListener('click', handleCreateAgent);
    closeEditAgentModalButton.addEventListener('click', () => toggleEditAgentModal(false));
    closeAgentModalButton.addEventListener('click', () => toggleAgentModal(false));
    closeModalButton.addEventListener('click', () => toggleSettingsModal(false));
    saveAgentButton.addEventListener('click', handleSaveAgent);
    imageStudioButton.addEventListener('click', () => {
        const imageAgents = agentsList.filter(name => name.includes('imagen'));
        populateImageAgentSelector(imageAgents);
        toggleImageStudioModal(true);
    });
    roboticsStudioButton.addEventListener('click', () => {
        const roboticsAgents = agentsList.filter(name => name.includes('robotics'));
        populateRoboticsAgentSelector(roboticsAgents);
        toggleRoboticsStudioModal(true);
    });
    musicStudioButton.addEventListener('click', () => {
        updateMusicStatus('Ready to generate music.');
        toggleMusicStudioModal(true);
    });
    videoStudioButton.addEventListener('click', () => {
        const videoAgents = agentsList.filter(name => name.includes('veo'));
        populateVideoAgentSelector(videoAgents);
        toggleVideoStudioModal(true);
    });
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

    // Image Studio Listeners
    generateImageButton.addEventListener('click', handleGenerateImages);
    closeImageStudioModalButton.addEventListener('click', () => toggleImageStudioModal(false));

    // Video Studio Listeners
    generateVideoButton.addEventListener('click', handleGenerateVideo);
    closeVideoStudioModalButton.addEventListener('click', () => toggleVideoStudioModal(false));

    // Robotics Studio Listeners
    processRoboticsImageButton.addEventListener('click', handleProcessRoboticsImage);
    closeRoboticsStudioModalButton.addEventListener('click', () => toggleRoboticsStudioModal(false));

    // Music Studio Listeners
    closeMusicStudioModalButton.addEventListener('click', () => {
        stopMusicStream();
        toggleMusicStudioModal(false);
    });
    startMusicButton.addEventListener('click', () => {
        setupMusicSocket();
        musicSocket.emit('start_music_stream', { prompt: musicPromptInput.value });
    });
    steerMusicButton.addEventListener('click', () => musicSocket.emit('steer_music', { prompt: musicSteerPromptInput.value }));
    stopMusicButton.addEventListener('click', stopMusicStream);
    imageCountSlider.addEventListener('input', () => document.getElementById('image-count-value').textContent = imageCountSlider.value);

    loadAgents();
    // After loading agents, trigger the mode loading for the default selected agent
    if (agentSelect.value) {
        handleAgentChange(agentSelect.value);
    }
}

initialize();
addMessage('assistant', 'Welcome to TinyAGI! Select an agent and start chatting.');