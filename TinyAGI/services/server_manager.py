# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/services/server_manager.py

from flask import Flask, request, jsonify, Response, g
from ..agent import AgentSystem
from ..utils import setup_logging
import logging

logger = logging.getLogger(__name__)


def create_app():
    """
    Create and configure the Flask application.

    :return: Configured Flask app
    """
    app = Flask(__name__)
    setup_logging()

    # Default agent name (ensure this matches an agent defined in your configuration)
    default_agent_name = 'ollama_agent'

    def initialize_agent_system(config_files='config/agent_config.json'):
        """Initializes the AgentSystem and attaches it to the app context."""
        agent_system = AgentSystem(config_files=config_files)
        agent_manager = agent_system.agent_manager
        agent = agent_manager.get_agent(default_agent_name)
        if not agent:
            logger.error(f"Default agent '{default_agent_name}' not found.")
            raise ValueError(f"Agent '{default_agent_name}' is not available.")
        
        app.agent_system = agent_system
        app.agent = agent
        app.config['AGENT_CONFIG'] = agent_system.config
        app.plugin_manager = agent_system.plugin_manager
        app.task_manager = agent_system.task_manager
        app.tool_manager = agent_system.tool_manager
        logger.info("AgentSystem initialized and attached to Flask app.")

    # Initial setup
    with app.app_context():
        initialize_agent_system()

    @app.route('/chat', methods=['POST'])
    def chat():
        """
        Handle chat requests.
        """
        data = request.get_json()
        messages = data.get('messages')
        inference_params = data.get('inference_params', {})
        stream = data.get('stream', False)

        if not messages:
            return jsonify({'error': 'Messages are required'}), 400

        # Build prompt from messages
        prompt = ''
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt += f"{role.capitalize()}: {content}\n"

        prompt += "Assistant:"

        try:
            if stream:
                def generate():
                    for chunk in app.agent.generate_text(prompt, stream=True):
                        yield chunk
                return Response(generate(), mimetype='text/plain')
            else:
                generated_text = app.agent.generate_text(prompt)
                return jsonify({'response': generated_text})
        except Exception as e:
            logger.error(f"Error during chat: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/generate', methods=['POST'])
    def generate():
        """
        Handle text generation requests.
        """
        data = request.get_json()
        prompt = data.get('prompt')
        inference_params = data.get('inference_params', {})
        stream = data.get('stream', False)

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        try:
            if stream:
                def generate_stream():
                    for chunk in app.agent.generate_text(prompt, stream=True):
                        yield chunk
                return Response(generate_stream(), mimetype='text/plain')
            else:
                generated_text = app.agent.generate_text(prompt)
                return jsonify({'response': generated_text})
        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/embed', methods=['POST'])
    def embed():
        """
        Handle embedding requests.
        """
        data = request.get_json()
        input_data = data.get('input')

        if not input_data:
            return jsonify({'error': 'Input text is required'}), 400

        try:
            embeddings = app.agent.embed(input_data)
            return jsonify({'embedding': embeddings})
        except Exception as e:
            logger.error(f"Error during embedding: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/reload', methods=['POST'])
    def reload_model():
        """
        Reload the model with new configuration.
        """
        data = request.get_json()
        config_file = data.get('config_file')
        if not config_file:
            return jsonify({'error': 'Config file path is required'}), 400

        try:
            # Re-initialize the agent system with the new config
            initialize_agent_system(config_files=config_file)
            return jsonify({'message': 'Model reloaded successfully'}), 200
        except Exception as e:
            logger.error(f"Error during model reload: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/config', methods=['GET'])
    def get_config():
        """
        Retrieve the current configuration.
        """
        return jsonify(app.config.get('AGENT_CONFIG', {})), 200

    return app

def run_server():
    """
    Run the Flask server.
    """
    app = create_app()
    app.run(debug=True)


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
