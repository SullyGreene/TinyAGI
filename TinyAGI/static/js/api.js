/**
 * Fetches the list of available agents from the server.
 * @returns {Promise<string[]>} A promise that resolves to an array of agent names.
 */
export async function fetchAgents() {
    const response = await fetch('/api/agents');
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

/**
 * Fetches the detailed configuration for a single agent.
 * @param {string} agentName - The name of the agent.
 * @returns {Promise<object>} A promise that resolves to the agent's configuration object.
 */
export async function fetchAgentDetails(agentName) {
    const response = await fetch(`/api/agents/${agentName}`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

/**
 * Deletes an agent from the server.
 * @param {string} agentName - The name of the agent to delete.
 * @returns {Promise<object>} A promise that resolves to the server's response message.
 */
export async function deleteAgent(agentName) {
    const response = await fetch(`/api/agents/${agentName}`, { method: 'DELETE' });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

/**
 * Sends updated agent data to the server.
 * @param {string} agentName - The original name of the agent to update.
 * @param {object} updateData - An object containing the fields to update.
 * @returns {Promise<object>} A promise that resolves to the server's response.
 */
export async function updateAgent(agentName, updateData) {
    const response = await fetch(`/api/agents/${agentName}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

/**
 * Sends data to create a new agent on the server.
 * @param {object} agentData - An object containing the new agent's properties.
 * @returns {Promise<object>} A promise that resolves to the server's response.
 */
export async function createAgent(agentData) {
    const response = await fetch('/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(agentData),
    });
    if (!response.ok) {
        const errorData = await response.json();
        // Use 409 for conflict (duplicate name)
        const errorMessage = response.status === 409 ? errorData.error : `HTTP error! status: ${response.status}`;
        throw new Error(errorData.error || errorMessage);
    }
    return await response.json();
}


/**
 * Sends a chat request to the server and returns a readable stream for the response.
 * @param {string} agent - The name of the agent to chat with.
 * @param {object[]} messages - The history of messages.
 * @param {object} settings - The generation settings (e.g., temperature).
 * @param {AbortSignal} signal - The AbortSignal to cancel the request.
 * @returns {Promise<ReadableStream>} A promise that resolves to a ReadableStream of the response.
 */
export async function streamChat(agent, messages, settings, signal) {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent, messages, stream: true, settings }),
        signal // Pass the signal to the fetch request
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    return response.body;
}