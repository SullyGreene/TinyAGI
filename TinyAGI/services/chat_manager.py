# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/services/chat_manager.py

import logging
from flask import Flask, request, jsonify, Response
from ..agent import AgentSystem
from ..utils import setup_logging

logger = logging.getLogger(__name__)

class ChatManager:
    def __init__(self, config_file='config/agent_config.json'):
        setup_logging()
        self.agent_system = AgentSystem(config_file)
        self.agent_manager = self.agent_system.agent_manager
        self.agent = self.agent_manager.get_agent('default_agent')
        if not self.agent:
            logger.error("Default agent not found.")
            raise ValueError("Default agent not found.")
        logger.info("ChatManager initialized.")

    def create_app(self):
        app = Flask(__name__)

        @app.route('/chat', methods=['POST'])
        def chat():
            data = request.get_json()
            messages = data.get('messages')
            stream = data.get('stream', False)

            if not messages:
                return jsonify({'error': 'Messages are required'}), 400

            # Build prompt
            prompt = ''
            for msg in messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                prompt += f"{role.capitalize()}: {content}\n"

            prompt += "Assistant:"

            try:
                if stream:
                    def generate():
                        for chunk in self.agent.generate_text(prompt, stream=True):
                            yield chunk
                    return Response(generate(), mimetype='text/plain')
                else:
                    response_text = self.agent.generate_text(prompt)
                    return jsonify({'response': response_text})
            except Exception as e:
                logger.error(f"Error during chat: {e}")
                return jsonify({'error': str(e)}), 500

        return app


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
