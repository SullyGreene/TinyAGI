// TinyAGI/static/js/features/ide-studio.js

import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import { streamChat } from '../api.js';
import { getSettings } from '../lib/settings.js';
import { toggleModal } from '../ui/modal.js';
import { showToast } from '../toast.js';

const ideStudioButton = document.getElementById('ide-studio-button');
const ideGenerateButton = document.getElementById('ide-generate-button');
const ideLanguageSelect = document.getElementById('ide-language-select');
const idePromptInput = document.getElementById('ide-prompt-input');
const ideOutputCode = document.getElementById('ide-output-code');

let abortController = null;

async function handleIDEGenerate() {
    const agentSelect = document.getElementById('agent-select'); // Use the main agent
    const prompt = idePromptInput.value;
    const language = ideLanguageSelect.value;
    const selectedAgent = agentSelect.value;

    if (!prompt) {
        showToast('Please enter a code generation prompt.', 'error');
        return;
    }

    // Construct a specialized prompt for code generation
    const fullPrompt = `You are an expert programmer. Generate a high-quality, production-ready code snippet in ${language} for the following task. Only output the code, with no extra explanation or markdown formatting.\n\nTask: ${prompt}`;
    const messages = [{ role: 'user', content: fullPrompt }];
    const settings = getSettings();

    ideGenerateButton.disabled = true;
    ideOutputCode.textContent = ''; // Clear previous content
    ideOutputCode.parentElement.classList.add('loading'); // Show spinner

    abortController = new AbortController();
    let fullResponse = '';

    try {
        const stream = await streamChat(selectedAgent, messages, messages[0], settings, null, null, abortController.signal);
        const reader = stream.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            fullResponse += chunk;

            // Update the code block's text content directly
            ideOutputCode.textContent = fullResponse;

            // Re-apply highlighting
            window.hljs.highlightElement(ideOutputCode);
        }
    } catch (error) {
        if (error.name !== 'AbortError') {
            console.error('Error generating code:', error);
            ideOutputCode.textContent = `// Error: ${error.message}`;
        }
    } finally {
        ideGenerateButton.disabled = false;
        ideOutputCode.parentElement.classList.remove('loading');
        abortController = null;
    }
}

export function initializeIDEStudio() {
    if (ideStudioButton) {
        ideStudioButton.addEventListener('click', () => {
            if (ideOutputCode && ideLanguageSelect) {
                ideOutputCode.className = `language-${ideLanguageSelect.value} hljs`;
            }
            toggleModal('ide-studio-modal', true)
        });
    }
    if (ideGenerateButton) {
        ideGenerateButton.addEventListener('click', handleIDEGenerate);
    }
    if (ideLanguageSelect) {
        ideLanguageSelect.addEventListener('change', () => {
            if (ideOutputCode) ideOutputCode.className = `language-${ideLanguageSelect.value}`;
        });
    }
}