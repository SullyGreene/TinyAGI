import pytest
import os
import logging
from TinyAGI.agents.gemma_agent import GemmaAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Skip tests if Gemini API key is not set
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
pytestmark = pytest.mark.skipif(not GEMINI_API_KEY, reason="GEMINI_API_KEY not set in environment")

@pytest.fixture(scope="module")
def gemma_agent():
    """Fixture to initialize the GemmaAgent once per test module."""
    logger.info("Initializing GemmaAgent for testing...")
    try:
        # Using a dictionary for config to avoid file I/O in tests
        model_config = {
            "name": "gemma-3n-e2b-it",
            "parameters": {
                "temperature": 0.5,
                "max_output_tokens": 150
            }
        }
        agent = GemmaAgent(model_config=model_config)
        logger.info("GemmaAgent initialized successfully.")
        return agent
    except Exception as e:
        pytest.fail(f"Failed to initialize GemmaAgent: {e}")

def test_generate_text(gemma_agent):
    """Test standard text generation with GemmaAgent."""
    logger.info("Testing standard text generation with Gemma...")
    prompt = "What is the main benefit of using a lightweight AI model like Gemma?"
    response = gemma_agent.generate_text(prompt)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 10
    logger.info(f"Gemma text generation test passed. Response: {response}")

def test_generate_text_stream(gemma_agent):
    """Test streaming text generation with GemmaAgent."""
    logger.info("Testing streaming text generation with Gemma...")
    prompt = "Write a one-sentence summary of the plot of 'The Hobbit'."
    response_stream = gemma_agent.generate_text(prompt, stream=True)
    full_response = "".join(chunk for chunk in response_stream)
    assert full_response is not None
    assert isinstance(full_response, str)
    assert len(full_response) > 0
    assert "Bilbo" in full_response or "hobbit" in full_response
    logger.info(f"Gemma streaming test passed. Response: {full_response}")

def test_generate_text_with_system_prompt(gemma_agent):
    """Test text generation with a system prompt with GemmaAgent."""
    logger.info("Testing text generation with a system prompt with Gemma...")
    system_prompt = "You are a friendly robot from the future. Your name is Gizmo."
    prompt = "What is your purpose?"
    response = gemma_agent.generate_text(prompt, system_prompt=system_prompt)
    assert response is not None
    assert isinstance(response, str)
    assert "Gizmo" in response or "robot" in response
    logger.info(f"Gemma system prompt test passed. Response: {response}")

def test_embed_not_implemented(gemma_agent):
    """Test that the embed method returns an empty list as it's not implemented."""
    logger.info("Testing embed method on GemmaAgent...")
    embedding = gemma_agent.embed("This is a test.")
    assert embedding == []
    logger.info("Gemma embed test passed as expected.")