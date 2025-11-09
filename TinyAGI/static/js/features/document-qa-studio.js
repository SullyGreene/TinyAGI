// TinyAGI/static/js/features/document-qa-studio.js

import { showToast } from '../toast.js';
import { toggleModal } from '../ui/modal.js';

const studioButton = document.getElementById('document-qa-button');
const agentSelect = document.getElementById('doc-qa-agent-select');
const fileUpload = document.getElementById('doc-qa-upload');
const questionInput = document.getElementById('doc-qa-question');
const askButton = document.getElementById('doc-qa-ask-button');
const answerContainer = document.getElementById('doc-qa-answer-container');
const statusBar = document.getElementById('doc-qa-status');

let currentDocId = null;

function setStatus(message, isError = false) {
    statusBar.textContent = message;
    statusBar.style.color = isError ? 'var(--accent-danger)' : 'var(--text-secondary)';
}

function populateAgentSelector(allAgents) {
    // Populate with all agents, as most can embed and chat
    agentSelect.innerHTML = '';
    if (allAgents.length === 0) {
        agentSelect.innerHTML = '<option>No agents found</option>';
        agentSelect.disabled = true;
    } else {
        allAgents.forEach(agentName => {
            const option = document.createElement('option');
            option.value = agentName;
            option.textContent = agentName;
            agentSelect.appendChild(option);
        });
        agentSelect.disabled = false;
    }
}

async function handleFileUpload() {
    const file = fileUpload.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('document', file);
    formData.append('agent', agentSelect.value);

    setStatus(`Processing "${file.name}"...`);
    questionInput.disabled = true;
    askButton.disabled = true;

    try {
        const response = await fetch('/api/documents/upload', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();
        if (!response.ok) throw new Error(result.error);

        currentDocId = result.doc_id;
        setStatus(`Ready to answer questions about "${file.name}".`);
        questionInput.disabled = false;
        askButton.disabled = false;
        showToast('Document processed successfully!', 'success');
    } catch (error) {
        setStatus(`Error: ${error.message}`, true);
        showToast(error.message, 'error');
    }
}

async function handleAskQuestion() {
    const question = questionInput.value.trim();
    if (!question || !currentDocId) return;

    askButton.disabled = true;
    answerContainer.innerHTML = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;

    try {
        const response = await fetch('/api/documents/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                doc_id: currentDocId,
                question: question,
                agent: agentSelect.value,
            }),
        });

        const result = await response.json();
        if (!response.ok) throw new Error(result.error);

        answerContainer.innerHTML = marked.parse(result.answer);
    } catch (error) {
        answerContainer.innerHTML = `<p style="color: var(--accent-danger);">Error: ${error.message}</p>`;
        showToast(error.message, 'error');
    } finally {
        askButton.disabled = false;
    }
}

export function initializeDocumentQAStudio(agentManager) {
    studioButton.addEventListener('click', () => toggleModal('document-qa-modal', true));
    fileUpload.addEventListener('change', handleFileUpload);
    askButton.addEventListener('click', handleAskQuestion);
    agentManager.setOnAgentChange((_, allAgents) => populateAgentSelector(allAgents));
}