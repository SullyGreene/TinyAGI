# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/ollama_agent.py

import logging
import json
import ollama
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class OllamaAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        self.client = ollama.Client(host=self.model_config.get('host', 'http://localhost:11434'))

        if 'model_card' in self.model_config:
            card_path = self.model_config['model_card']
            try:
                with open(card_path, 'r') as f:
                    card_data = json.load(f)
                self.model_name = card_data.get('name', 'gemma:2b')
                self.parameters.update(card_data.get('parameters', {}))
                logger.info(f"Loaded model card: {card_path}")
            except FileNotFoundError:
                logger.error(f"Model card not found at {card_path}. Using default model name.")
                self.model_name = self.model_config.get('name', 'gemma:2b')
        else:
            self.model_name = self.model_config.get('name', 'gemma:2b')
        
        logger.info(f"OllamaAgent initialized with model: {self.model_name}")

    def chat(self, messages, stream=False, **kwargs):
        """Handles a chat conversation with history using Ollama."""
        mode = kwargs.pop('mode', None)
        return self.generate_text(messages, stream=stream, mode=mode, **kwargs)

    def generate_text(self, messages, stream=False, **kwargs):
        """
        Generates text using the Ollama model.
        The 'messages' parameter is used directly as it's the expected format.
        """
        try:
            mode = kwargs.pop('mode', None)
            mode_config = self.model_config.get('modes', {}).get(mode, {})

            # The Ollama library uses a 'system' message for system prompts.
            system_prompt = mode_config.get('system_prompt')
            final_messages = list(messages)
            if system_prompt:
                # Check if a system message already exists
                has_system = any(m.get('role') == 'system' for m in final_messages)
                if not has_system:
                    final_messages.insert(0, {'role': 'system', 'content': system_prompt})

            # Parameter precedence: base -> mode -> runtime
            generation_params = self.parameters.copy()
            if 'parameters' in mode_config:
                generation_params.update(mode_config.get('parameters', {}))
            generation_params.update(kwargs)

            # Map common names to Ollama's expected names
            if 'temperature' in generation_params:
                generation_params['temperature'] = float(generation_params['temperature'])
            if 'max_tokens' in generation_params:
                generation_params['num_predict'] = int(generation_params.pop('max_tokens'))

            response = self.client.chat(
                model=self.model_name,
                messages=final_messages,
                stream=stream,
                options=generation_params
            )

            if stream:
                return (chunk['message']['content'] for chunk in response)
            else:
                return response['message']['content']
        except Exception as e:
            logger.error(f"Error generating text with Ollama: {e}", exc_info=True)
            return f"An error occurred with Ollama: {e}"

    def embed(self, input_data):
        """Generates embeddings using the Ollama model."""
        try:
            response = ollama.embeddings(model=self.model_name, prompt=input_data)
            return response["embedding"]
        except Exception as e:
            logger.error(f"Error generating embeddings with Ollama: {e}", exc_info=True)
            return []