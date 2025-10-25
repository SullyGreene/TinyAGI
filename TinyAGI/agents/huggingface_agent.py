# TinyAGI/agents/huggingface_agent.py

from .base_agent import BaseAgent
from transformers import pipeline

class HuggingFaceAgent(BaseAgent):
    def __init__(self, name: str, description: str, model_name: str = "distilgpt2"):
        super().__init__(name, description)
        self.model_name = model_name
        self.generator = pipeline("text-generation", model=self.model_name)

    def generate_text(self, prompt: str, **kwargs) -> str:
        return self.generator(prompt, max_length=50, num_return_sequences=1)[0]["generated_text"]
