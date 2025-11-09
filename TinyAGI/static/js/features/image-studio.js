// TinyAGI/static/js/features/image-studio.js

import { generateImages } from '../api.js';
import { showToast } from '../toast.js';
import { toggleModal } from '../ui/modal.js';

const imageStudioButton = document.getElementById('image-studio-button');
const generateImageButton = document.getElementById('generate-image-button');
const imageAgentSelect = document.getElementById('image-agent-select');
const imagePrompt = document.getElementById('image-prompt');
const imageCountSlider = document.getElementById('image-count-slider');
const imageAspectRatioSelect = document.getElementById('image-aspect-ratio');
const resultsPanel = document.getElementById('image-results-panel');

function populateImageAgentSelector(allAgents) {
    if (!imageAgentSelect) return;

    const imageAgents = allAgents.filter(name => name.includes('imagen')); // Simple filter
    imageAgentSelect.innerHTML = '';
    if (imageAgents.length === 0) {
        imageAgentSelect.innerHTML = '<option>No image agents found</option>';
        imageAgentSelect.disabled = true;
    } else {
        imageAgents.forEach(agentName => {
            const option = document.createElement('option');
            option.value = agentName;
            option.textContent = agentName;
            imageAgentSelect.appendChild(option);
        });
        imageAgentSelect.disabled = false;
    }
}

function showImageGenerationSpinner() {
    resultsPanel.innerHTML = `<div class="typing-indicator" style="margin: auto;"><span></span><span></span><span></span></div>`;
}

function displayGeneratedImages(imagesBase64) {
    resultsPanel.innerHTML = '';
    imagesBase64.forEach(base64String => {
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${base64String}`;
        resultsPanel.appendChild(img);
    });
}

async function handleGenerateImages() {
    const agent = imageAgentSelect.value;
    const prompt = imagePrompt.value.trim();
    const settings = {
        number_of_images: parseInt(imageCountSlider.value, 10),
        aspect_ratio: imageAspectRatioSelect.value
    };

    if (!prompt) {
        showToast('Please enter a prompt.', 'error');
        return;
    }

    showImageGenerationSpinner();
    generateImageButton.disabled = true;

    try {
        const result = await generateImages(agent, prompt, settings);
        displayGeneratedImages(result.images);
    } catch (error) {
        showToast(`Error generating images: ${error.message}`, 'error');
        resultsPanel.innerHTML = `<p style="color: var(--accent-danger);">Failed to generate images.</p>`;
    } finally {
        generateImageButton.disabled = false;
    }
}

export function initializeImageStudio(agentManager) {
    imageStudioButton.addEventListener('click', () => {
        toggleModal('image-studio-modal', true);
    });
    generateImageButton.addEventListener('click', handleGenerateImages);
    imageCountSlider.addEventListener('input', () => document.getElementById('image-count-value').textContent = imageCountSlider.value);
    agentManager.setOnAgentChange((_, allAgents) => populateImageAgentSelector(allAgents));
}