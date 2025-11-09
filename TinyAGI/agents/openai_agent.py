# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/openai_agent.py

import logging
import os
import openai
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class OpenAIAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables.")
            raise ValueError("OPENAI_API_KEY is required for OpenAIAgent.")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = self.model_config.get('model', 'gpt-5-nano')
        logger.info(f"OpenAIAgent initialized with model: {self.model_name}")

    def _format_chat_history(self, messages):
        """
        Formats a list of messages for the OpenAI Responses API.
        Maps 'system' to 'developer' role.
        """
        history = []
        for message in messages:
            role = message.get("role")
            content = message.get("content")
            if role and content:
                # The new API uses 'developer' for system-level instructions.
                mapped_role = "developer" if role == "system" else role
                history.append({"role": mapped_role, "content": content})
        return history

    def chat(self, messages, stream=False, **kwargs):
        """Handles a chat conversation with history using the Responses API."""
        mode = kwargs.pop('mode', None)
        return self.generate_text(messages, stream=stream, mode=mode, **kwargs)

    def generate_text(self, messages, stream=False, **kwargs):
        """Generates text using the OpenAI model."""
        try:
            mode = kwargs.pop('mode', None)
            mode_config = self.model_config.get('modes', {}).get(mode, {})

            # The 'instructions' parameter is for high-level instructions.
            # We'll use the system prompt from the mode or settings here.
            instructions = mode_config.get('system_prompt')
            if 'system_prompt' in kwargs:
                instructions = kwargs.pop('system_prompt')

            # Format messages for the 'input' parameter
            formatted_messages = self._format_chat_history(messages)

            # Parameter precedence: base -> mode -> runtime
            generation_params = self.parameters.copy()
            if 'parameters' in mode_config:
                generation_params.update(mode_config.get('parameters', {}))
            generation_params.update(kwargs)

            # The Responses API uses a 'reasoning' object for some controls.
            # We'll map temperature to it for now.
            reasoning_config = {}
            if 'temperature' in generation_params:
                reasoning_config['effort'] = 'low' # A default, can be configured

            response = self.client.responses.create(
                model=self.model_name,
                input=formatted_messages,
                instructions=instructions,
                reasoning=reasoning_config if reasoning_config else None,
                stream=stream
            )

            if stream:
                def stream_generator():
                    for chunk in response:
                        # The new API has a different streaming format.
                        # We need to check for text content in the delta.
                        if chunk.delta and chunk.delta.content and chunk.delta.content[0].text:
                            yield chunk.delta.content[0].text
                return stream_generator()
            else:
                # The output_text property conveniently aggregates text output.
                return response.output_text
        except Exception as e:
            logger.error(f"Error generating text with OpenAI: {e}", exc_info=True)
            error_message = f"An error occurred with OpenAI: {e}"
            return iter([error_message]) if stream else error_message

    def embed(self, input_data):
        """Generates embeddings using the OpenAI embedding models."""
        # This would use client.embeddings.create, similar to gemini_agent.
        logger.warning("Embedding is not yet implemented for OpenAIAgent.")
        return []