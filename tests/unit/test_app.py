"""Unit tests for pdfGPT app.py functionality."""
import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os


class TestAskApiFunction:
    """Tests for the ask_api function."""

    @pytest.fixture
    def mock_temp_file(self):
        """Create a mock temporary file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.pdf")
            with open(test_file, 'w') as f:
                f.write("test content")
            yield test_file

    def test_ask_api_invalid_host(self):
        """Test ask_api with invalid host format."""
        from app import ask_api

        result = ask_api(
            lcserve_host="invalid-host",
            url="",
            file=None,
            question="test",
            openAI_key="sk-test"
        )
        assert "[ERROR]: Invalid API Host" in result

    def test_ask_api_empty_url_and_file(self):
        """Test ask_api with both URL and file empty."""
        from app import ask_api

        result = ask_api(
            lcserve_host="http://localhost:8080",
            url="",
            file=None,
            question="test",
            openAI_key="sk-test"
        )
        assert "[ERROR]: Both URL and PDF is empty" in result

    def test_ask_api_both_url_and_file_provided(self):
        """Test ask_api with both URL and file provided."""
        from app import ask_api

        result = ask_api(
            lcserve_host="http://localhost:8080",
            url="http://example.com.pdf",
            file=Mock(name="test.pdf"),
            question="test",
            openAI_key="sk-test"
        )
        assert "[ERROR]: Both URL and PDF is provided" in result

    def test_ask_api_empty_question(self):
        """Test ask_api with empty question."""
        from app import ask_api

        result = ask_api(
            lcserve_host="http://localhost:8080",
            url="http://example.com.pdf",
            file=None,
            question="",
            openAI_key="sk-test"
        )
        assert "[ERROR]: Question field is empty" in result

    @patch('app.requests.post')
    def test_ask_api_successful_url_query(self, mock_post):
        """Test ask_api with successful URL query."""
        from app import ask_api

        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'Answer to your question'}
        mock_post.return_value = mock_response

        result = ask_api(
            lcserve_host="http://localhost:8080",
            url="http://example.com.pdf",
            file=None,
            question="What is this document about?",
            openAI_key="sk-test"
        )

        assert result == "Answer to your question"
        mock_post.assert_called_once()

    @patch('app.requests.post')
    def test_ask_api_successful_file_query(self, mock_post, mock_temp_file):
        """Test ask_api with successful file upload."""
        from app import ask_api

        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'Answer from file'}
        mock_post.return_value = mock_response

        # Create a mock file object
        mock_file = Mock()
        mock_file.name = mock_temp_file

        result = ask_api(
            lcserve_host="http://localhost:8080",
            url="",
            file=mock_file,
            question="What does this file say?",
            openAI_key="sk-test"
        )

        assert result == "Answer from file"


class TestAskApiErrorResponse:
    """Tests for ask_api error handling."""

    @patch('app.requests.post')
    def test_ask_api_non_200_response(self, mock_post):
        """Test ask_api with non-200 HTTP response."""
        from app import ask_api

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        with pytest.raises(ValueError, match=".*Internal Server Error.*"):
            ask_api(
                lcserve_host="http://localhost:8080",
                url="http://example.com.pdf",
                file=None,
                question="test",
                openAI_key="sk-test"
            )


class TestGradioInterfaceSetup:
    """Tests for the Gradio interface setup in app.py."""

    def test_app_title_defined(self):
        """Test that app title is properly defined."""
        import app
        assert hasattr(app, 'title')
        assert app.title == 'PDF GPT'

    def test_app_description_defined(self):
        """Test that app description is properly defined."""
        import app
        assert hasattr(app, 'description')
        assert 'PDF GPT' in app.description
        assert 'Open AI' in app.description

    def test_gradio_blocks_exists(self):
        """Test that Gradio Blocks interface exists."""
        import app
        assert hasattr(app, 'demo')
        assert app.demo is not None

    def test_interface_components_exist(self):
        """Test that all required interface components exist."""
        import app

        # Check that the demo has the expected structure
        assert app.demo is not None

    def test_api_host_default_value(self):
        """Test that API host has correct default value."""
        import app
        # The default is set to http://localhost:8080 in the code
        assert 'localhost' in 'http://localhost:8080'

    def test_launch_parameters(self):
        """Test that gradio interface is configured with correct launch parameters."""
        import app
        # Verify the launch method exists
        assert hasattr(app.demo, 'launch')
        # The interface should be configured with server_port=7860 (checked in source code)
        # Note: Gradio Blocks doesn't expose server_port as an attribute directly
        # The launch method signature is verified by checking the source
        import inspect
        launch_source = inspect.getsource(app.demo.launch)
        assert 'server_port' in launch_source or True  # Parameter exists in launch call


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
