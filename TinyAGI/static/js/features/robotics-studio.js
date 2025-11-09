// TinyAGI/static/js/features/robotics-studio.js

import { processRoboticsImage } from '../api.js';
import { showToast } from '../toast.js';
import { toggleModal } from '../ui/modal.js';

const roboticsStudioButton = document.getElementById('robotics-studio-button');
const processButton = document.getElementById('process-robotics-image-button');
const agentSelect = document.getElementById('robotics-agent-select');
const imageUpload = document.getElementById('robotics-image-upload');
const promptInput = document.getElementById('robotics-prompt');
const resultsPanel = document.getElementById('robotics-results-panel');

function populateRoboticsAgentSelector(allAgents) {
    const roboticsAgents = allAgents.filter(name => name.includes('robotics'));
    agentSelect.innerHTML = '';
    if (roboticsAgents.length === 0) {
        agentSelect.innerHTML = '<option>No robotics agents found</option>';
        agentSelect.disabled = true;
    } else {
        roboticsAgents.forEach(agentName => {
            const option = document.createElement('option');
            option.value = agentName;
            option.textContent = agentName;
            agentSelect.appendChild(option);
        });
        agentSelect.disabled = false;
    }
}

function showRoboticsSpinner() {
    resultsPanel.innerHTML = `<div class="typing-indicator" style="margin: auto;"><span></span><span></span><span></span></div>`;
}

function displayRoboticsResult(imageFile, resultJsonString) {
    resultsPanel.innerHTML = '';
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        try {
            const results = JSON.parse(resultJsonString);
            results.forEach(item => {
                if (item.point) {
                    const [y, x] = item.point;
                    ctx.beginPath();
                    ctx.arc((x / 1000) * canvas.width, (y / 1000) * canvas.height, 10, 0, 2 * Math.PI, false);
                    ctx.fillStyle = 'rgba(255, 0, 0, 0.7)';
                    ctx.fill();
                }
            });
        } catch (e) {
            console.error("Error parsing robotics result:", e);
        }
        resultsPanel.appendChild(canvas);
    };
    img.src = URL.createObjectURL(imageFile);
}

async function handleProcessImage() {
    const imageFile = imageUpload.files[0];
    if (!imageFile) {
        showToast('Please upload an image.', 'error');
        return;
    }
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('prompt', promptInput.value.trim());
    formData.append('agent', agentSelect.value);

    showRoboticsSpinner();
    processButton.disabled = true;
    try {
        const result = await processRoboticsImage(formData);
        displayRoboticsResult(imageFile, result.result);
    } catch (error) {
        showToast(`Error processing image: ${error.message}`, 'error');
    } finally {
        processButton.disabled = false;
    }
}

export function initializeRoboticsStudio(agentManager) {
    roboticsStudioButton.addEventListener('click', () => toggleModal('robotics-studio-modal', true));
    processButton.addEventListener('click', handleProcessImage);
    agentManager.setOnAgentChange((_, allAgents) => populateRoboticsAgentSelector(allAgents));
}