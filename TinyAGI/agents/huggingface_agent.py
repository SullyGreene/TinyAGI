# TinyAGI/agents/huggingface_agent.py

from .base_agent import BaseAgent
from transformers import pipeline

class HuggingFaceAgent(BaseAgent):
    def __init__(self, model_config, module_manager=None):
        super().__init__(model_config)
        self.model_name = self.model_config.get('model_name', 'distilgpt2')
        self.generator = pipeline("text-generation", model=self.model_name)

    def generate_text(self, prompt: str, **kwargs) -> str:
        return self.generator(prompt, max_length=50, num_return_sequences=1)[0]["generated_text"]
