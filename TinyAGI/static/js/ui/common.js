// TinyAGI/static/js/ui/common.js

const agentSelect = document.getElementById('agent-select');
const promptInput = document.getElementById('prompt-input');
const sendButton = document.getElementById('send-button');

/**
 * Populates the agent selection dropdown.
 * @param {string[]} agentNames - An array of agent names.
 */
export function populateAgentSelector(agentNames) {
    agentSelect.innerHTML = ''; // Clear loading text
    agentNames.forEach(agentName => {
        const option = document.createElement('option');
        option.value = agentName;
        option.textContent = agentName;
        agentSelect.appendChild(option);
    });
    // Enable the form now that agents are loaded
    promptInput.disabled = false;
    sendButton.disabled = promptInput.value.trim() === '';
}

/**
 * Populates the mode selection dropdown based on the selected agent's capabilities.
 * @param {object} modes - An object where keys are mode IDs and values are mode details.
 */
export function populateModeSelector(modes) {
    const modeSelect = document.getElementById('mode-select');
    modeSelect.innerHTML = '<option value="">Default</option>'; // Reset with default

    if (modes && Object.keys(modes).length > 0) {
        for (const modeId in modes) {
            const option = document.createElement('option');
            option.value = modeId;
            option.textContent = modes[modeId].name || modeId; // Use name if available, else ID
            modeSelect.appendChild(option);
        }
        modeSelect.disabled = false;
    } else {
        modeSelect.disabled = true;
    }
}

/**
 * Handles errors during agent loading.
 */
export function handleAgentError() {
    agentSelect.innerHTML = '<option>Error loading agents</option>';
}