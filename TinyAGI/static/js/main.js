// TinyAGI/static/js/main.js

import { initializeChat } from './chat.js';
import { initializeAgentManager } from './features/agent-manager.js';
import { initializeImageStudio } from './features/image-studio.js';
import { initializeVideoStudio } from './features/video-studio.js';
import { initializeMusicStudio } from './features/music-studio.js';
import { initializeRoboticsStudio } from './features/robotics-studio.js';
import { initializeIDEStudio } from './features/ide-studio.js';
import { initializeSettings } from './features/settings.js';
import { applyTheme, initializeTheme } from './ui/theme.js';
import { applySidebarState, initializeSidebar } from './ui/sidebar.js';
import { initializeModal } from './ui/modal.js';

/**
 * Main initialization function for the entire application.
 */
async function initialize() {
    // Apply initial UI states
    applyTheme();
    applySidebarState();

    // Initialize core UI components
    initializeTheme();
    initializeSidebar();
    ['settings-modal', 'agent-modal', 'edit-agent-modal', 'create-agent-modal', 'image-studio-modal', 'video-studio-modal', 'music-studio-modal', 'robotics-studio-modal', 'ide-studio-modal'].forEach(initializeModal);

    // Initialize feature modules
    initializeSettings();
    const agentManager = initializeAgentManager();
    initializeImageStudio(agentManager);
    initializeVideoStudio(agentManager);
    initializeMusicStudio();
    initializeRoboticsStudio(agentManager);
    initializeIDEStudio();

    // Initialize the chat system
    initializeChat();

    // Load initial data
    await agentManager.loadAgents();
}

document.addEventListener('DOMContentLoaded', initialize);