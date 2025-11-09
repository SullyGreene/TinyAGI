// TinyAGI/static/js/features/video-studio.js

import { startVideoGeneration, pollVideoOperation } from '../api.js';
import { showToast } from '../toast.js';
import { toggleModal } from '../ui/modal.js';

const videoStudioButton = document.getElementById('video-studio-button');
const generateVideoButton = document.getElementById('generate-video-button');
const videoAgentSelect = document.getElementById('video-agent-select');
const videoPrompt = document.getElementById('video-prompt');
const videoDurationSelect = document.getElementById('video-duration-select');
const resultContainer = document.getElementById('video-result-container');

function populateVideoAgentSelector(allAgents) {
    if (!videoAgentSelect) return;

    const videoAgents = allAgents.filter(name => name.includes('veo')); // Simple filter
    videoAgentSelect.innerHTML = '';
    if (videoAgents.length === 0) {
        videoAgentSelect.innerHTML = '<option>No video agents found</option>';
        videoAgentSelect.disabled = true;
    } else {
        videoAgents.forEach(agentName => {
            const option = document.createElement('option');
            option.value = agentName;
            option.textContent = agentName;
            videoAgentSelect.appendChild(option);
        });
        videoAgentSelect.disabled = false;
    }
}

function showVideoGenerationSpinner() {
    resultContainer.innerHTML = `<div style="text-align: center; padding: 2rem;">
        <div class="typing-indicator" style="margin: auto;"><span></span><span></span><span></span></div>
        <p style="margin-top: 1rem; color: var(--text-secondary);">Generating video... This may take several minutes.</p>
    </div>`;
}

function displayVideoResult(videoUrl) {
    resultContainer.innerHTML = `<video controls autoplay loop style="width: 100%; border-radius: 8px;">
        <source src="${videoUrl}" type="video/mp4">
        Your browser does not support the video tag.
    </video>`;
}

async function handleGenerateVideo() {
    const agent = videoAgentSelect.value;
    const prompt = videoPrompt.value.trim();
    if (!prompt) {
        showToast('Please enter a prompt for the video.', 'error');
        return;
    }

    showVideoGenerationSpinner();
    generateVideoButton.disabled = true;

    try {
        const startResponse = await startVideoGeneration(agent, prompt, { duration_seconds: videoDurationSelect.value });
        const pollInterval = setInterval(async () => {
            const statusResponse = await pollVideoOperation(startResponse.operation_name);
            if (statusResponse.status === 'complete') {
                clearInterval(pollInterval);
                displayVideoResult(statusResponse.url);
                generateVideoButton.disabled = false;
            } else if (statusResponse.status === 'failed') {
                clearInterval(pollInterval);
                showToast(`Video generation failed: ${statusResponse.error}`, 'error');
                resultContainer.innerHTML = `<p style="color: var(--accent-danger);">Video generation failed.</p>`;
                generateVideoButton.disabled = false;
            }
        }, 10000); // Poll every 10 seconds
    } catch (error) {
        showToast(`Error starting video generation: ${error.message}`, 'error');
        resultContainer.innerHTML = `<p style="color: var(--accent-danger);">Could not start video generation.</p>`;
        generateVideoButton.disabled = false;
    }
}

export function initializeVideoStudio(agentManager) {
    videoStudioButton.addEventListener('click', () => toggleModal('video-studio-modal', true));
    generateVideoButton.addEventListener('click', handleGenerateVideo);
    agentManager.setOnAgentChange((_, allAgents) => populateVideoAgentSelector(allAgents));
}