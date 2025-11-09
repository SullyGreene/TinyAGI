// TinyAGI/static/js/ui/modal.js

const modals = {};

/**
 * Toggles the visibility of a modal.
 * @param {string} modalId - The ID of the modal element.
 * @param {boolean} show - True to show, false to hide.
 */
export function toggleModal(modalId, show) {
    if (!modals[modalId]) {
        modals[modalId] = document.getElementById(modalId);
    }
    const modal = modals[modalId];
    if (modal) {
        modal.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Initializes close button listeners for a modal.
 * @param {string} modalId - The ID of the modal element.
 */
export function initializeModal(modalId) {
    const closeButton = document.querySelector(`#${modalId} .close-button`);
    if (closeButton) {
        closeButton.addEventListener('click', () => toggleModal(modalId, false));
    }
}