// TinyAGI/static/js/chat.js

import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import { streamChat, fetchConversations, fetchConversationMessages } from './api.js';
import { 
    populateConversationHistory, 
    setActiveConversation,
    addMessageToUI,
    showThinkingIndicator,
    updateAssistantMessage,
    setFormDisabled,
    clearChatWindow,
    toggleStopButton,
    checkWelcomeScreen
} from './ui.js';

let messages = [];
let currentConversationId = null;
let abortController = null;

function adjustTextareaHeight(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
}

async function loadConversations() {
    const conversationHistoryContainer = document.getElementById('conversation-history-container');
    try {
        const conversations = await fetchConversations();
        populateConversationHistory(conversations, currentConversationId);
    } catch (error) {
        console.error("Could not load conversations:", error);
        if (conversationHistoryContainer) {
            conversationHistoryContainer.innerHTML = '<p class="error-text">Could not load history.</p>';
        }
    }
}

async function handleSend() {
    const promptInput = document.getElementById('prompt-input');
    const agentSelect = document.getElementById('agent-select');
    const modeSelect = document.getElementById('mode-select');
    const systemPromptTextarea = document.getElementById('system-prompt');

    const prompt = promptInput.value.trim();
    if (!prompt) return;

    const userMessage = { role: 'user', content: prompt };
    const selectedAgent = agentSelect.value;
    const selectedMode = modeSelect.value;
    
    // Retrieve settings from UI elements
    const settings = {
        temperature: parseFloat(document.getElementById('temperature-slider').value),
        max_tokens: parseInt(document.getElementById('max-tokens-slider').value, 10),
        system_prompt: systemPromptTextarea.value.trim()
    };

    checkWelcomeScreen();
    addMessageToUI('user', prompt);
    messages.push(userMessage);
    promptInput.value = '';
    adjustTextareaHeight(promptInput);
    setFormDisabled(true);
    toggleStopButton(true);

    const assistantContentDiv = showThinkingIndicator();
    let assistantResponse = '';
    abortController = new AbortController();

    const messagesForContext = [...messages];
    if (settings.system_prompt) {
        messagesForContext.unshift({ role: 'system', content: settings.system_prompt });
    }

    try {
        const stream = await streamChat(selectedAgent, messagesForContext, userMessage, settings, selectedMode, currentConversationId, abortController.signal);
        const reader = stream.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let firstChunk = true;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            if (firstChunk && currentConversationId === null) {
                const idMatch = buffer.match(/^conversation_id:(\d+)\n/);
                if (idMatch) {
                    const newId = parseInt(idMatch[1], 10);
                    if (!isNaN(newId)) {
                        currentConversationId = newId;
                        console.log(`Started new conversation: ${currentConversationId}`);
                        buffer = buffer.substring(idMatch[0].length);
                        loadConversations(); // Refresh history list
                    }
                }
            }
            firstChunk = false;

            if (buffer) {
                assistantResponse += buffer;
                updateAssistantMessage(assistantContentDiv, marked.parse(assistantResponse));
                buffer = '';
            }
        }
        messages.push({ role: 'assistant', content: assistantResponse });
    } catch (error) {
        if (error.name === 'AbortError') {
            const stoppedMessage = assistantResponse + ' [Stopped]';
            updateAssistantMessage(assistantContentDiv, marked.parse(stoppedMessage));
            messages.push({ role: 'assistant', content: stoppedMessage });
        } else {
            console.error('Error sending message:', error);
            updateAssistantMessage(assistantContentDiv, `**Error:**\n\nSorry, an error occurred: ${error.message}`);
        }
    } finally {
        setFormDisabled(false);
        toggleStopButton(false);
        promptInput.focus();
        abortController = null;
    }
}

function handleClearChat() {
    messages = [];
    currentConversationId = null;
    clearChatWindow();
    checkWelcomeScreen();
    setActiveConversation(null);
    console.log('New chat started.');
}

function handleStop() {
    if (abortController) {
        abortController.abort();
    }
}

async function handleConversationClick(event) {
    const conversationItem = event.target.closest('.conversation-item');
    if (!conversationItem) return;

    const conversationId = parseInt(conversationItem.dataset.id, 10);
    if (isNaN(conversationId) || conversationId === currentConversationId) return;

    try {
        const conversation = await fetchConversationMessages(conversationId);
        clearChatWindow();
        messages = conversation.messages;
        messages.forEach(msg => addMessageToUI(msg.role, msg.content));
        currentConversationId = conversation.id;
        setActiveConversation(conversation.id);
        checkWelcomeScreen();
    } catch (error) {
        console.error(`Failed to load conversation ${conversationId}:`, error);
        alert(`Error: ${error.message}`);
    }
}

function handleCopyClick(event) {
    if (!event.target.classList.contains('copy-button')) return;

    const button = event.target;
    const preElement = button.closest('pre');
    const contentDiv = button.closest('.content');

    const textToCopy = preElement ? preElement.querySelector('code').innerText : contentDiv.dataset.rawText;

    navigator.clipboard.writeText(textToCopy).then(() => {
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = 'Copy';
        }, 2000);
    }).catch(err => console.error('Failed to copy text: ', err));
}

export function initializeChat() {
    const sendButton = document.getElementById('send-button');
    const clearChatButton = document.getElementById('new-chat-button');
    const stopButton = document.getElementById('stop-button');
    const conversationHistoryContainer = document.getElementById('conversation-history-container');
    const promptInput = document.getElementById('prompt-input');
    const chatWindow = document.getElementById('chat-window');

    sendButton.addEventListener('click', handleSend);
    clearChatButton.addEventListener('click', handleClearChat);
    stopButton.addEventListener('click', handleStop);
    conversationHistoryContainer.addEventListener('click', handleConversationClick);
    chatWindow.addEventListener('click', handleCopyClick);

    promptInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });
    promptInput.addEventListener('input', () => adjustTextareaHeight(promptInput));

    loadConversations();
    checkWelcomeScreen();
}