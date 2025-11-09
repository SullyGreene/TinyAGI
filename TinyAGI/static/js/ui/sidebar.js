// TinyAGI/static/js/ui/sidebar.js

const sidebar = document.getElementById('sidebar');
const sidebarToggleButton = document.getElementById('sidebar-toggle');
const sidebarOverlay = document.getElementById('sidebar-overlay');
const SIDEBAR_STATE_KEY = 'tinyagi_sidebar_state';

/**
 * Applies the saved sidebar state from localStorage or defaults to 'expanded'.
 */
export function applySidebarState() {
    if (!sidebar) return;

    const savedState = localStorage.getItem(SIDEBAR_STATE_KEY) || 'expanded';
    sidebar.className = savedState;
    updateSidebarIcon(savedState);
}

/**
 * Toggles the sidebar state between 'expanded' and 'collapsed'.
 */
function toggleSidebar() {
    if (!sidebar) return;

    const isExpanded = sidebar.classList.contains('expanded');
    const newState = isExpanded ? 'collapsed' : 'expanded';
    sidebar.className = newState;
    localStorage.setItem(SIDEBAR_STATE_KEY, newState);
    updateSidebarIcon(newState);

    // Handle overlay for mobile
    if (window.innerWidth <= 768) {
        if (newState === 'expanded') {
            sidebarOverlay.style.visibility = 'visible';
            sidebarOverlay.style.opacity = '1';
            sidebarOverlay.style.transition = 'opacity var(--transition-med)';
        } else {
            sidebarOverlay.style.opacity = '0';
            sidebarOverlay.style.transition = 'opacity var(--transition-med), visibility 0s var(--transition-med)';
            sidebarOverlay.style.visibility = 'hidden';
        }
    }
}

function updateSidebarIcon(state) {
    if (!sidebarToggleButton) return;
    const collapseIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>`;
    const expandIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>`;
    sidebarToggleButton.innerHTML = state === 'expanded' ? collapseIcon : expandIcon;
}

export function initializeSidebar() {
    if (sidebarToggleButton) {
        sidebarToggleButton.addEventListener('click', toggleSidebar);
    }
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', () => {
            if (sidebar.classList.contains('expanded')) {
                toggleSidebar();
            }
        });
    }
}