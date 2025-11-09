document.addEventListener('DOMContentLoaded', () => {
    const agentSelect = document.getElementById('agent-select');
    const chatWindow = document.getElementById('chat-window');
    const promptInput = document.getElementById('prompt-input');
    const sendButton = document.getElementById('send-button');

    let messages = [];

    // Fetch agents and populate the dropdown
    async function loadAgents() {
        try {
            const response = await fetch('/api/agents');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const agents = await response.json();
            
            agentSelect.innerHTML = ''; // Clear loading text
            agents.forEach(agentName => {
                const option = document.createElement('option');
                option.value = agentName;
                option.textContent = agentName;
                agentSelect.appendChild(option);
            });
        } catch (error) {
            console.error("Could not load agents:", error);
            agentSelect.innerHTML = '<option>Error loading agents</option>';
        }
    }

    function addMessageToUI(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'content';
        contentDiv.textContent = content;
        
        messageDiv.appendChild(contentDiv);
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll
    }

    async function handleSend() {
        const prompt = promptInput.value.trim();
        if (!prompt) return;

        const selectedAgent = agentSelect.value;
        if (!selectedAgent || selectedAgent === 'Error loading agents') {
            alert('Please select a valid agent.');
            return;
        }

        addMessageToUI('user', prompt);
        messages.push({ role: 'user', content: prompt });
        promptInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent: selectedAgent,
                    messages: messages,
                    stream: false // Streaming UI is more complex, starting with non-stream
                })
            });

            const data = await response.json();
            const assistantResponse = data.response || `Error: ${data.error}`;
            addMessageToUI('assistant', assistantResponse);
            messages.push({ role: 'assistant', content: assistantResponse });

        } catch (error) {
            console.error('Error sending message:', error);
            addMessageToUI('assistant', 'Sorry, an error occurred.');
        }
    }

    sendButton.addEventListener('click', handleSend);
    promptInput.addEventListener('keypress', (e) => e.key === 'Enter' && handleSend());

    loadAgents();
});