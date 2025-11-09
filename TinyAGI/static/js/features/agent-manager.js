// TinyAGI/static/js/features/agent-manager.js

import { fetchAgents, deleteAgent, fetchAgentDetails, updateAgent, createAgent, fetchModels } from '../api.js';
import { showToast } from '../toast.js';
import { toggleModal } from '../ui/modal.js';
import { populateAgentSelector, populateModeSelector, handleAgentError } from '../ui.js';

const agentSelect = document.getElementById('agent-select');
const agentListContainer = document.getElementById('agent-list-container');
const createAgentTypeSelect = document.getElementById('create-agent-type');

let agentsList = [];
let onAgentChangeCallback;

function populateAgentManagerList(activeAgentName) {
    if (!agentListContainer) return;
    agentListContainer.innerHTML = ''; // Clear previous list
    
    agentsList.forEach(agentName => {
        const agentItem = document.createElement('div');
        agentItem.className = 'agent-item';
        if (agentName === activeAgentName) {
            agentItem.classList.add('active');
        }
        agentItem.dataset.agentName = agentName;
        
        const agentNameSpan = document.createElement('div');
        agentNameSpan.textContent = agentName;
        agentNameSpan.className = 'agent-name-selectable';
        
        const agentActions = document.createElement('div');
        agentActions.className = 'agent-item-actions';
        
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.className = 'button-secondary agent-edit-button';
        editButton.dataset.agentName = agentName;
        
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'button-danger agent-delete-button';
        deleteButton.dataset.agentName = agentName;
        
        agentActions.appendChild(editButton);
        agentActions.appendChild(deleteButton);
        
        agentItem.appendChild(agentNameSpan);
        agentItem.appendChild(agentActions);
        agentListContainer.appendChild(agentItem);
    });
}

async function loadAgents() {
    try {
        agentsList = await fetchAgents();
        populateAgentSelector(agentsList);
        populateAgentManagerList(agentSelect.value);
        if (agentSelect.value) {
            handleAgentChange(agentSelect.value);
        }
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
        if (onAgentChangeCallback) {
            onAgentChangeCallback(agentName, agentsList);
        }
    } catch (error) {
        console.error(`Could not load modes for agent ${agentName}:`, error);
        populateModeSelector({}); // Clear the modes dropdown on error
    }
}

async function handleDeleteAgent(agentName) {
    if (!confirm(`Are you sure you want to delete the agent "${agentName}"? This cannot be undone.`)) {
        return;
    }
    try {
        const result = await deleteAgent(agentName);
        showToast(result.message, 'success');
        await loadAgents();
    } catch (error) {
        console.error(`Failed to delete agent ${agentName}:`, error);
        showToast(`Error: ${error.message}`, 'error');
    }
}

async function handleEditAgent(agentName) {
    try {
        const agentDetails = await fetchAgentDetails(agentName);
        document.getElementById('edit-agent-name-title').textContent = agentDetails.name;
        document.getElementById('edit-agent-original-name').value = agentDetails.name;
        document.getElementById('edit-agent-description').value = agentDetails.description || '';
        document.getElementById('edit-agent-system-prompt').value = agentDetails.system_prompt || '';
        document.getElementById('edit-agent-model').value = agentDetails.model || (agentDetails.config ? agentDetails.config.generation_model : '');
        toggleModal('edit-agent-modal', true);
    } catch (error) {
        console.error(`Failed to fetch details for agent ${agentName}:`, error);
        showToast(`Error: ${error.message}`, 'error');
    }
}

async function handleSaveAgent() {
    const originalName = document.getElementById('edit-agent-original-name').value;
    const updateData = {
        description: document.getElementById('edit-agent-description').value,
        model: document.getElementById('edit-agent-model').value,
        system_prompt: document.getElementById('edit-agent-system-prompt').value,
    };

    try {
        const result = await updateAgent(originalName, updateData);
        showToast(result.message, 'success');
        toggleModal('edit-agent-modal', false);
        await loadAgents();
    } catch (error) {
        console.error(`Failed to update agent ${originalName}:`, error);
        showToast(`Error: ${error.message}`, 'error');
    }
}

async function handleCreateAgent() {
    const name = document.getElementById('create-agent-name').value.trim();
    if (!name) {
        showToast('Agent Name is required.', 'error');
        return;
    }
    const modelInput = document.getElementById('create-agent-model-input') || document.getElementById('create-agent-model-select');
    const agentData = {
        name,
        type: document.getElementById('create-agent-type').value,
        description: document.getElementById('create-agent-description').value,
        model: modelInput.value,
        system_prompt: document.getElementById('create-agent-system-prompt').value,
    };

    try {
        const result = await createAgent(agentData);
        showToast(result.message, 'success');
        toggleModal('create-agent-modal', false);
        await loadAgents();
    } catch (error) {
        console.error(`Failed to create agent:`, error);
        showToast(`Error: ${error.message}`, 'error');
    }
}

function handleAgentSelection(event) {
    const target = event.target;
    if (target.classList.contains('agent-delete-button')) {
        handleDeleteAgent(target.dataset.agentName);
    } else if (target.classList.contains('agent-edit-button')) {
        handleEditAgent(target.dataset.agentName);
    } else if (target.closest('.agent-name-selectable')) {
        const agentName = target.closest('.agent-item').dataset.agentName;
        agentSelect.value = agentName;
        populateAgentManagerList(agentName);
        toggleModal('agent-modal', false);
        handleAgentChange(agentName);
    }
}

function resetCreateAgentForm() {
    document.getElementById('create-agent-name').value = '';
    document.getElementById('create-agent-description').value = '';
    document.getElementById('create-agent-system-prompt').value = '';
    handleCreateAgentTypeChange();
}

async function handleCreateAgentTypeChange() {
    // This function was improved in the previous step to fetch models from the API
    // It's kept here as part of the agent creation feature.
    const agentType = createAgentTypeSelect.value;
    const modelContainer = document.getElementById('create-agent-model-container');
    modelContainer.innerHTML = '<span class="loader"></span>';
    try {
        const models = await fetchModels(agentType);
        if (models.length > 0) {
            let selectHTML = '<select id="create-agent-model-select">';
            models.forEach(model => selectHTML += `<option value="${model}">${model}</option>`);
            selectHTML += '</select>';
            modelContainer.innerHTML = selectHTML;
        } else {
            modelContainer.innerHTML = `<input type="text" id="create-agent-model-input" placeholder="Enter model name...">`;
        }
    } catch (error) {
        console.error(`Failed to fetch models for ${agentType}:`, error);
        showToast(`Could not load models for ${agentType}.`, 'error');
        modelContainer.innerHTML = `<input type="text" id="create-agent-model-input" placeholder="Enter model name...">`;
    }
}

export function initializeAgentManager() {
    document.getElementById('manage-agents-button').addEventListener('click', () => {
        populateAgentManagerList(agentSelect.value);
        toggleModal('agent-modal', true);
    });
    document.getElementById('create-agent-button').addEventListener('click', () => {
        resetCreateAgentForm();
        toggleModal('create-agent-modal', true);
    });
    agentSelect.addEventListener('change', (e) => handleAgentChange(e.target.value));
    agentListContainer.addEventListener('click', handleAgentSelection);
    document.getElementById('save-agent-button').addEventListener('click', handleSaveAgent);
    document.getElementById('confirm-create-agent-button').addEventListener('click', handleCreateAgent);
    createAgentTypeSelect.addEventListener('change', handleCreateAgentTypeChange);

    return {
        loadAgents,
        setOnAgentChange: (callback) => { onAgentChangeCallback = callback; },
    };
}