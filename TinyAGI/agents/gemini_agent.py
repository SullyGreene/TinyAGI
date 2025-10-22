# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/gemini_agent.py

import logging
import os
import google.generativeai as genai
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class GeminiAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        api_key = os.getenv('GEMINI_API_KEY', '')
        if not api_key:
            logger.error("Gemini API key not provided.")
            raise ValueError("Gemini API key is required.")
        genai.configure(api_key=api_key)
        
        # Set up the generation model
        self.generation_model_name = self.model_config.get('generation_model', 'gemini-2.5-flash')
        self.model_name = self.generation_model_name # For BaseAgent logging
        self.model = genai.GenerativeModel(self.generation_model_name)
        
        # Set up the embedding model
        self.embedding_model_name = self.model_config.get('embedding_model', 'models/embedding-001')
        logger.info(f"GeminiAgent initialized with generation model: {self.generation_model_name} and embedding model: {self.embedding_model_name}")

    def generate_text(self, prompt, stream=False):
        try:
            response = self.model.generate_content(
                prompt,
                stream=stream,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.parameters.get('candidate_count', 1),
                    stop_sequences=self.parameters.get('stop_sequences', None),
                    max_output_tokens=self.parameters.get('max_output_tokens', 150),
                    temperature=self.parameters.get('temperature', 0.7),
                    top_p=self.parameters.get('top_p', None),
                    top_k=self.parameters.get('top_k', None),
                )
            )
            # Handle cases where the response is blocked by safety settings
            if not response.parts:
                logger.warning(f"Gemini response was blocked. Reason: {response.prompt_feedback.block_reason}. Safety Ratings: {response.prompt_feedback.safety_ratings}")
                return None if not stream else iter([])

            if stream:
                return (chunk.text for chunk in response)
            else:
                return response.text
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {e}")
            return None

    def embed(self, input_data):
        try:
            if isinstance(input_data, str):
                input_data = [input_data]
            result = genai.embed_content(
                model=self.embedding_model_name,
                content=input_data,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embeddings with Gemini: {e}")
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
