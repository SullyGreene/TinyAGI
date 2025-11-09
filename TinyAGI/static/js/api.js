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