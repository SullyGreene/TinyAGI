# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/robotics_agent.py

import logging
import os
import google.generativeai as genai
from google.generativeai import types
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class RoboticsAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is required for RoboticsAgent.")
        
        genai.configure(api_key=api_key)

        self.model_name = self.model_config.get('model', 'gemini-robotics-er-1.5-preview')
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"RoboticsAgent initialized with model: {self.model_name}")

    def process_image_with_prompt(self, image_part, prompt, **kwargs):
        """
        Processes an image with a given prompt and returns the structured output.
        """
        try:
            # Default config for robotics tasks
            config = types.GenerateContentConfig(
                temperature=kwargs.get('temperature', 0.5),
                thinking_config=types.ThinkingConfig(thinking_budget=kwargs.get('thinking_budget', 0))
            )
            
            response = self.model.generate_content(
                contents=[image_part, prompt],
                generation_config=config
            )
            return response.text
        except Exception as e:
            logger.error(f"Error processing with RoboticsAgent: {e}", exc_info=True)
            raise