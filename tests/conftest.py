"""pytest configuration for pdfGPT tests."""
import pytest


@pytest.fixture
def sample_api_host():
    """Sample API host fixture."""
    return "http://localhost:8080"


@pytest.fixture
def sample_openai_key():
    """Sample OpenAI key fixture."""
    return "sk-test-key-12345"


@pytest.fixture
def sample_question():
    """Sample question fixture."""
    return "What is the main topic of this document?"
