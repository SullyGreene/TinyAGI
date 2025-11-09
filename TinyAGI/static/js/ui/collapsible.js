// TinyAGI/static/js/ui/collapsible.js

export function initializeCollapsibles() {
    const sections = document.querySelectorAll('.sidebar-collapsible-section');

    sections.forEach(section => {
        const header = section.querySelector('.sidebar-section-header');
        if (header) {
            header.addEventListener('click', () => {
                section.classList.toggle('collapsed');
            });
        }
    });
}