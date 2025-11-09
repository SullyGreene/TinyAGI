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
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is required for GeminiAgent.")
        genai.configure(api_key=api_key)

        self.generation_model_name = self.model_config.get('generation_model', 'gemini-1.5-flash')
        self.embedding_model_name = self.model_config.get('embedding_model', 'models/embedding-001')
        self.generation_model = genai.GenerativeModel(self.generation_model_name)
        
        logger.info(f"GeminiAgent initialized with generation model: {self.generation_model_name} and embedding model: {self.embedding_model_name}")

    def _format_chat_history(self, messages):
        """Formats a list of messages for the Gemini API."""
        history = []
        # The Gemini API expects roles 'user' and 'model'.
        # We map 'assistant' to 'model'.
        for message in messages:
            role = message.get("role")
            content = message.get("content")
            if role and content:
                mapped_role = "model" if role == "assistant" else role
                history.append({"role": mapped_role, "parts": [content]})
        
        # The last message is the current prompt, so we separate it from the history.
        if history and history[-1]["role"] == "user":
            current_prompt = history.pop()["parts"][0]
            return current_prompt, history
        elif history and history[-1]["role"] == "model":
             # This case is unusual, but we can handle it.
             return "What is your response?", history
        
        return "Hello", [] # Default if messages is empty or malformed

    def chat(self, messages, stream=False, **kwargs):
        """Handles a chat conversation with history."""
        mode = kwargs.pop('mode', None)
        prompt, history = self._format_chat_history(messages)
        
        # The genai library's chat object is stateful. We can start a new one for each turn.
        chat_session = self.generation_model.start_chat(history=history)
        
        # Pass through other kwargs to generate_text
        return self.generate_text(prompt, stream=stream, mode=mode, chat_session=chat_session, **kwargs)

    def generate_text(self, prompt, stream=False, system_prompt=None, chat_session=None, **kwargs):
        """Generates text using the Gemini model."""
        try:
            mode = kwargs.pop('mode', None)
            mode_config = self.model_config.get('modes', {}).get(mode, {})

            final_system_prompt = mode_config.get('system_prompt', system_prompt)

            model_instance = self.generation_model
            if final_system_prompt:
                model_instance = genai.GenerativeModel(
                    self.generation_model_name,
                    system_instruction=final_system_prompt
                )

            generation_params = self.parameters.copy()
            if 'parameters' in mode_config:
                generation_params.update(mode_config.get('parameters', {}))
            generation_params.update(kwargs)

            if 'max_tokens' in generation_params:
                generation_params['max_output_tokens'] = generation_params.pop('max_tokens')

            # Use the provided chat session if available, otherwise generate directly
            target = chat_session if chat_session else model_instance
            response = target.send_message(
                prompt,
                stream=stream,
                generation_config=genai.types.GenerationConfig(**generation_params)
            )

            if stream:
                return (chunk.text for chunk in response)
            else:
                return response.text
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {e}", exc_info=True)
            return f"An error occurred: {e}"

    def embed(self, input_data):
        """Generates embeddings for the given input data."""
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
            logger.error(f"Error generating embeddings with Gemini: {e}", exc_info=True)
            return []