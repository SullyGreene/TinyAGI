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

    def generate_text(self, prompt, stream=False, system_prompt=None):
        try:
            model = self.model
            if system_prompt:
                model = genai.GenerativeModel(self.model_name, system_instruction=system_prompt)

            response = model.generate_content(
                prompt,
                stream=stream,
                generation_config=genai.types.GenerationConfig(**self.parameters)
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