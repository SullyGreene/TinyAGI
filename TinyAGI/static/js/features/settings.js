// TinyAGI/static/js/features/settings.js

import { loadSettings, saveSettings, getSettings } from '../lib/settings.js';
import { toggleModal } from '../ui/modal.js';
import { showToast } from '../toast.js';

const settingsButton = document.getElementById('settings-button');
const saveSettingsButton = document.getElementById('save-settings-button');
const temperatureSlider = document.getElementById('temperature-slider');
const temperatureValue = document.getElementById('temperature-value');
const maxTokensSlider = document.getElementById('max-tokens-slider');
const maxTokensValue = document.getElementById('max-tokens-value');
const systemPromptTextarea = document.getElementById('system-prompt');

function updateTemperatureDisplay() {
    if (temperatureValue) {
        temperatureValue.textContent = parseFloat(temperatureSlider.value).toFixed(1);
    }
}

function updateMaxTokensDisplay() {
    if (maxTokensValue) {
        maxTokensValue.textContent = maxTokensSlider.value;
    }
}

function populateSettingsForm() {
    const currentSettings = getSettings();
    temperatureSlider.value = currentSettings.temperature;
    maxTokensSlider.value = currentSettings.max_tokens;
    systemPromptTextarea.value = currentSettings.system_prompt;
    updateTemperatureDisplay();
    updateMaxTokensDisplay();
}

function handleSaveSettings() {
    const currentSettings = getSettings();
    currentSettings.temperature = parseFloat(temperatureSlider.value);
    currentSettings.max_tokens = parseInt(maxTokensSlider.value, 10);
    currentSettings.system_prompt = systemPromptTextarea.value;
    saveSettings();
    toggleModal('settings-modal', false);
    showToast('Settings saved successfully!', 'success');
}

export function initializeSettings() {
    // Load settings from localStorage on startup
    loadSettings();

    if (settingsButton) {
        settingsButton.addEventListener('click', () => {
            populateSettingsForm();
            toggleModal('settings-modal', true);
        });
    }

    if (saveSettingsButton) {
        saveSettingsButton.addEventListener('click', handleSaveSettings);
    }

    temperatureSlider.addEventListener('input', updateTemperatureDisplay);
    maxTokensSlider.addEventListener('input', updateMaxTokensDisplay);
}