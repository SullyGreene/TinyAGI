# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/veo_agent.py

import logging
import os
import google.generativeai as genai
from google.generativeai import types
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class VeoAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is required for VeoAgent.")
        
        genai.configure(api_key=api_key)

        self.model_name = self.model_config.get('model', 'veo-3.1-generate-preview')
        logger.info(f"VeoAgent initialized with model: {self.model_name}")

    def generate_video(self, prompt, **kwargs):
        """
        Starts the video generation process and returns the operation object.
        This is an asynchronous operation.
        """
        try:
            config_params = {
                'resolution': kwargs.get('resolution', '720p'),
                'duration_seconds': int(kwargs.get('duration_seconds', 8))
            }
            
            operation = genai.generate_video(
                model=self.model_name,
                prompt=prompt,
                generation_config=types.GenerateVideoConfig(**config_params)
            )
            return operation
        except Exception as e:
            logger.error(f"Error starting video generation with Veo: {e}", exc_info=True)
            raise