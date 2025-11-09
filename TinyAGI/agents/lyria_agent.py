# MIT License
# Copyright (c) 2024 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/agents/lyria_agent.py

import logging
import os
import asyncio
import google.generativeai as genai
from google.generativeai import types
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class LyriaAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is required for LyriaAgent.")
        
        # The Lyria model is experimental and may require a specific API version
        self.client = genai.Client(http_options={'api_version': 'v1alpha'})
        self.model_name = self.model_config.get('model', 'models/lyria-realtime-exp')
        logger.info(f"LyriaAgent initialized with model: {self.model_name}")

    async def connect_and_stream(self, output_queue, initial_prompt):
        """
        Connects to the Lyria RealTime service and streams audio chunks to a queue.
        This method is designed to be run as a long-lived async task.
        """
        logger.info("Connecting to Lyria RealTime...")
        try:
            async with self.client.aio.live.music.connect(model=self.model_name) as session:
                # Put the session object in the queue so the parent can control it
                await output_queue.put(session)

                # Send initial prompt
                await session.set_weighted_prompts(prompts=[types.WeightedPrompt(text=initial_prompt, weight=1.0)])
                await session.play()

                # Stream audio chunks
                async for message in session.receive():
                    if message.server_content and message.server_content.audio_chunks:
                        audio_data = message.server_content.audio_chunks[0].data
                        await output_queue.put(audio_data)
        except Exception as e:
            logger.error(f"Error in Lyria connection: {e}", exc_info=True)
            await output_queue.put(e) # Signal error to the listener