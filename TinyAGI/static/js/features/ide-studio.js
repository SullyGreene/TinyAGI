// TinyAGI/static/js/features/ide-studio.js

import { toggleModal } from '../ui/modal.js';
import { showToast } from '../toast.js';

const ideStudioButton = document.getElementById('ide-studio-button');
const ideGenerateButton = document.getElementById('ide-generate-button');
const ideLanguageSelect = document.getElementById('ide-language-select');
const idePromptInput = document.getElementById('ide-prompt-input');
const ideOutputCode = document.getElementById('ide-output-code');

function handleIDEGenerate() {
    const prompt = idePromptInput.value;
    const language = ideLanguageSelect.value;
    const fullPrompt = `Generate a code snippet in ${language} for the following task:\n\n${prompt}`;

    // In a real implementation, this would call the chat API.
    // For now, it's a placeholder.
    console.log("IDE Generation Request:", { language, prompt });
    showToast("IDE code generation is not fully implemented yet.", 'info');

    ideOutputCode.textContent = `// Code generation for "${prompt}" in ${language} would appear here.`;
    window.hljs.highlightElement(ideOutputCode);
}

export function initializeIDEStudio() {
    ideStudioButton.addEventListener('click', () => toggleModal('ide-studio-modal', true));
    ideGenerateButton.addEventListener('click', handleIDEGenerate);
    ideLanguageSelect.addEventListener('change', () => {
        ideOutputCode.className = `language-${ideLanguageSelect.value}`;
    });
}