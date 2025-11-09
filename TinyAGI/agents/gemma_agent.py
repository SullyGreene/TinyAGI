# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/gemma_agent.py

import logging
import os
import json
import google.generativeai as genai
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class GemmaAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        api_key = os.getenv('GEMINI_API_KEY', '')
        if not api_key:
            logger.error("Gemini API key not provided for GemmaAgent.")
            raise ValueError("Gemini API key is required to use GemmaAgent.")
        genai.configure(api_key=api_key)

        # Load model card if provided
        if 'model_card' in self.model_config:
            card_path = self.model_config['model_card']
            try:
                with open(card_path, 'r') as f:
                    card_data = json.load(f)
                self.model_name = card_data.get('name', 'gemma-3n-e2b-it')
                self.parameters.update(card_data.get('parameters', {}))
                logger.info(f"Loaded model card: {card_path}")
            except FileNotFoundError:
                logger.error(f"Model card not found at {card_path}. Using default model name.")
                self.model_name = self.model_config.get('name', 'gemma-3n-e2b-it')
        else:
            self.model_name = self.model_config.get('name', 'gemma-3n-e2b-it')

        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"GemmaAgent initialized with model: {self.model_name}")

    def _format_chat_history(self, messages):
        """
        Formats a list of message dictionaries into a single string prompt
        or a list suitable for the model's chat history.

        :param messages: A list of dictionaries, e.g., [{"role": "user", "content": "Hello"}]
        :return: A formatted string or list for the model.
        """
        # For Gemma via Gemini API, we can pass the history directly.
        # We need to map 'assistant' role to 'model'.
        history = []
        for message in messages:
            role = message.get("role")
            content = message.get("content")
            if role and content:
                # The Gemini API expects the role to be 'user' or 'model'
                mapped_role = "model" if role == "assistant" else role
                history.append({"role": mapped_role, "parts": [content]})
        
        # The last message is the current prompt, so we separate it.
        if history and history[-1]["role"] == "user":
            current_prompt = history.pop()["parts"][0]
            return current_prompt, history
        elif history and history[-1]["role"] == "model":
             # This case is odd (ending on assistant message), but we can handle it.
             return "What is your response?", history
        
        return "Hello", [] # Default if messages is empty or malformed

    def chat(self, messages, stream=False, **kwargs):
        """
        Handles a chat conversation with history.
        """
        prompt, history = self._format_chat_history(messages)
        self.model._history = history # Set the history on the model instance
        return self.generate_text(prompt, stream=stream, **kwargs)

    def generate_text(self, prompt, stream=False, system_prompt=None, **kwargs):
        try:
            model = self.model
            if system_prompt:
                model = genai.GenerativeModel(self.model_name, system_instruction=system_prompt)

            # Merge agent's default parameters with runtime kwargs
            generation_params = self.parameters.copy()
            generation_params.update(kwargs)

            # The Gemini API uses 'max_output_tokens', but a common name is 'max_tokens'.
            # We'll map it for convenience.
            if 'max_tokens' in generation_params:
                generation_params['max_output_tokens'] = generation_params.pop('max_tokens')

            response = model.generate_content(
                prompt,
                stream=stream,
                generation_config=genai.types.GenerationConfig(**generation_params)
            )

            if not response.parts:
                block_reason = "Unknown"
                if hasattr(response, 'prompt_feedback'):
                    block_reason = response.prompt_feedback.block_reason
                logger.warning(f"Gemma response was blocked. Reason: {block_reason}.")
                return "Response was blocked due to safety settings."

            if stream:
                return (chunk.text for chunk in response)
            else:
                return response.text
        except Exception as e:
            logger.error(f"Error generating text with Gemma: {e}")
            return None

    def embed(self, input_data):
        logger.warning("Embedding is not implemented for GemmaAgent.")
        return []


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