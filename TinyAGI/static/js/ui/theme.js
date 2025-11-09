// TinyAGI/static/js/ui/theme.js

const themeToggleButton = document.getElementById('theme-toggle-button');
const THEME_KEY = 'tinyagi_theme';

/**
 * Applies the saved theme from localStorage or defaults to 'dark'.
 */
export function applyTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
    document.body.dataset.theme = savedTheme;
    updateThemeIcon(savedTheme);
}

/**
 * Toggles the color theme between 'light' and 'dark'.
 */
function toggleTheme() {
    const currentTheme = document.body.dataset.theme || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.body.dataset.theme = newTheme;
    localStorage.setItem(THEME_KEY, newTheme);
    updateThemeIcon(newTheme);
}

/**
 * Updates the theme toggle button icon.
 * @param {string} theme - The current theme ('light' or 'dark').
 */
function updateThemeIcon(theme) {
    if (!themeToggleButton) return;
    const sunIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.64 5.64c-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41l1.06 1.06c.39.39 1.02.39 1.41 0s.39-1.02 0-1.41L5.64 5.64zm12.72 12.72c-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41l1.06 1.06c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41l-1.06-1.06zM5.64 18.36c.39.39.39 1.02 0 1.41-.39.39-1.02.39-1.41 0l-1.06-1.06c-.39-.39-.39-1.02 0-1.41s1.02-.39 1.41 0l1.06 1.06zm12.72-12.72c.39.39.39 1.02 0 1.41-.39.39-1.02.39-1.41 0l-1.06-1.06c-.39-.39-.39-1.02 0-1.41s1.02-.39 1.41 0l1.06 1.06z"/></svg>`;
    const moonIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-3.31 0-6-2.69-6-6 0-1.82.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>`;
    themeToggleButton.innerHTML = theme === 'dark' ? sunIcon : moonIcon;
}

export function initializeTheme() {
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', toggleTheme);
    }
}