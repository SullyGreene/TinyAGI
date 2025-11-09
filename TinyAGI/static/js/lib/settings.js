// TinyAGI/static/js/lib/settings.js

const SETTINGS_KEY = 'tinyagi_chat_settings';

let settings = {
    temperature: 1.0,
    max_tokens: 4096,
    system_prompt: ''
};

/**
 * Loads settings from localStorage into the module's state.
 */
export function loadSettings() {
    const savedSettings = localStorage.getItem(SETTINGS_KEY);
    if (savedSettings) {
        try {
            const parsedSettings = JSON.parse(savedSettings);
            // Merge with defaults to handle new settings added in future versions
            settings = { ...settings, ...parsedSettings };
            console.log('Loaded settings from localStorage:', settings);
        } catch (e) {
            console.error('Failed to parse settings from localStorage:', e);
        }
    }
}

/**
 * Saves the current settings state to localStorage.
 */
export function saveSettings() {
    try {
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
        console.log('Settings saved to localStorage:', settings);
    } catch (e) {
        console.error('Failed to save settings to localStorage:', e);
    }
}

/**
 * Returns the current settings object.
 * @returns {object} The settings object.
 */
export function getSettings() {
    return settings;
}