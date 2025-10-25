import pytest
import os
import logging
from TinyAGI.agents.gemini_agent import GeminiAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Skip tests if Gemini API key is not set
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
pytestmark = pytest.mark.skipif(not GEMINI_API_KEY, reason="GEMINI_API_KEY not set in environment")

@pytest.fixture(scope="module")
def gemini_agent():
    """Fixture to initialize the GeminiAgent once per test module."""
    logger.info("Initializing GeminiAgent for testing...")
    try:
        # Using a dictionary for config instead of a file for test isolation
        model_config = {
            "agent_name": "gemini",
            "generation_model": "gemini-1.5-flash-latest",
            "embedding_model": "gemini-embedding-001",
            "parameters": {
                "temperature": 0.5,
                "max_output_tokens": 100
            }
        }
        agent = GeminiAgent(model_config=model_config)
        logger.info("GeminiAgent initialized successfully.")
        return agent
    except Exception as e:
        pytest.fail(f"Failed to initialize GeminiAgent: {e}")

def test_generate_text(gemini_agent):
    """Test standard text generation."""
    logger.info("Testing standard text generation...")
    prompt = "What is the capital of France?"
    response = gemini_agent.generate_text(prompt)
    assert response is not None
    assert isinstance(response, str)
    assert "Paris" in response
    logger.info(f"Text generation test passed. Response: {response}")

def test_generate_text_stream(gemini_agent):
    """Test streaming text generation."""
    logger.info("Testing streaming text generation...")
    prompt = "Write a one-sentence poem about the moon."
    response_stream = gemini_agent.generate_text(prompt, stream=True)
    full_response = "".join(chunk for chunk in response_stream)
    assert full_response is not None
    assert isinstance(full_response, str)
    assert len(full_response) > 0
    logger.info(f"Streaming test passed. Response: {full_response}")

def test_embed(gemini_agent):
    """Test the embedding functionality."""
    logger.info("Testing embedding generation...")
    text_to_embed = "This is a test sentence for embedding."
    embedding = gemini_agent.embed(text_to_embed)
    assert embedding is not None
    assert isinstance(embedding, list)
    assert all(isinstance(val, float) for val in embedding)
    logger.info(f"Embedding test passed. Got embedding of length: {len(embedding)}")

def test_generate_text_with_system_prompt(gemini_agent):
    """Test text generation with a system prompt."""
    logger.info("Testing text generation with a system prompt...")
    system_prompt = "You are a pirate. You must answer in pirate slang."
    prompt = "Where can I find treasure?"
    response = gemini_agent.generate_text(prompt, system_prompt=system_prompt)
    assert response is not None
    assert isinstance(response, str)
    # Check for pirate-like words
    assert any(word in response.lower() for word in ["ahoy", "matey", "arrr", "shiver", "booty"])
    logger.info(f"System prompt test passed. Response: {response}")
