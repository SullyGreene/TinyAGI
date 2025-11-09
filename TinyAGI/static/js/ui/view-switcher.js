// TinyAGI/static/js/ui/view-switcher.js

let currentView = 'chat-view';

/**
 * Switches the main content area to the specified view.
 * @param {string} viewId - The ID of the studio view to switch to.
 */
export function switchView(viewId) {
    if (currentView === viewId) return;

    const oldView = document.getElementById(currentView);
    const newView = document.getElementById(viewId);
    const sidebarButtons = document.querySelectorAll('.sidebar-button');

    if (oldView) oldView.classList.remove('active');
    if (newView) newView.classList.add('active');

    // Update active state on sidebar buttons
    sidebarButtons.forEach(button => {
        button.classList.remove('active');
        if (button.dataset.view === viewId) {
            button.classList.add('active');
        }
    });

    currentView = viewId;
}

export function initializeViewSwitcher() {
    const sidebarButtons = document.querySelectorAll('.sidebar-button[data-view]');
    sidebarButtons.forEach(button => {
        button.addEventListener('click', () => {
            switchView(button.dataset.view);
        });
    });
}