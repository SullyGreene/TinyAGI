# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/imagen_agent.py

import logging
import os
import base64
from io import BytesIO
import google.generativeai as genai
from google.generativeai import types
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ImagenAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is required for ImagenAgent.")
        
        # The standard genai client does not have `models.generate_images`.
        # We assume the user has a version of the library that supports it,
        # or we use the appropriate client setup. For now, we'll use the standard configure.
        genai.configure(api_key=api_key)

        self.model_name = self.model_config.get('model', 'imagen-4.0-generate-001')
        logger.info(f"ImagenAgent initialized with model: {self.model_name}")

    def generate_images(self, prompt, **kwargs):
        """Generates images using the Imagen model and returns them as base64 strings."""
        try:
            # Extract and prepare config for the API call
            config_params = {
                'number_of_images': kwargs.get('number_of_images', 1),
                'aspect_ratio': kwargs.get('aspect_ratio', '1:1')
            }
            
            response = genai.generate_images(
                model=self.model_name,
                prompt=prompt,
                # The API expects a GenerateImagesConfig object
                generation_config=types.GenerateImagesConfig(**config_params)
            )

            base64_images = []
            for generated_image in response.images:
                # The image data is in the `_image_bytes` attribute.
                # We save it to a buffer and encode it.
                buffer = BytesIO(generated_image._image_bytes)
                encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
                base64_images.append(encoded_string)
            
            return base64_images
        except Exception as e:
            logger.error(f"Error generating images with Imagen: {e}", exc_info=True)
            # Propagate the error to be handled by the server
            raise