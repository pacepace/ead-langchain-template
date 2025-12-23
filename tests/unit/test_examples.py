"""
Tests for example scripts.

This demonstrates testing LLM application code without making actual API calls.
Uses mocking to test business logic, configuration, and error handling.

Run these tests with: pytest tests/unit/test_examples.py -v
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import Mock

# Add examples to path
examples_dir = Path(__file__).parent.parent.parent / "examples"
sys.path.insert(0, str(examples_dir))


def load_example_module(filename):
    """
    Load an example module dynamically.

    :param filename: Example filename (e.g., '01_basic.py')
    :ptype filename: str
    :return: Loaded module
    :rtype: module
    """
    filepath = examples_dir / filename
    spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# Load modules once for testing
basic_01 = load_example_module("01_basic.py")
streaming_02 = load_example_module("02_streaming.py")
conversation_03 = load_example_module("03_conversation.py")
advanced_04 = load_example_module("04_advanced.py")


class TestBasicExampleModule:
    """Tests for 01_basic.py structure and imports."""

    def test_module_has_required_functions(self):
        """
        Test that basic module exports expected functions.

        :return: None
        :rtype: None
        """
        assert hasattr(basic_01, "basic_openai_example")
        assert hasattr(basic_01, "basic_anthropic_example")
        assert hasattr(basic_01, "basic_gemini_example")
        assert hasattr(basic_01, "main")
        assert callable(basic_01.main)

    def test_module_imports_langchain_providers(self):
        """
        Test that module imports required LangChain classes.

        :return: None
        :rtype: None
        """
        assert hasattr(basic_01, "ChatOpenAI")
        assert hasattr(basic_01, "ChatAnthropic")
        assert hasattr(basic_01, "ChatGoogleGenerativeAI")

    def test_module_imports_langchain_llm_utilities(self):
        """
        Test that module imports our custom utilities.

        :return: None
        :rtype: None
        """
        assert hasattr(basic_01, "get_api_key")
        assert hasattr(basic_01, "get_logger")
        assert hasattr(basic_01, "get_model_name")
        assert hasattr(basic_01, "load_env_config")
        assert hasattr(basic_01, "setup_logging")


class TestBasicExampleFunctions:
    """Tests for 01_basic.py function behavior."""

    def test_basic_openai_example_with_mock(self, mock_env_vars, monkeypatch, capsys):
        """
        Test basic_openai_example with mocked LLM.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        # Create mock LLM
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "Machine learning is a subset of AI."
        mock_llm.invoke.return_value = mock_response

        # Mock ChatOpenAI to return our mock
        mock_chat_class = Mock(return_value=mock_llm)
        monkeypatch.setattr(basic_01, "ChatOpenAI", mock_chat_class)

        # Run function
        basic_01.basic_openai_example()

        # Verify ChatOpenAI was instantiated
        mock_chat_class.assert_called_once()
        call_kwargs = mock_chat_class.call_args.kwargs

        # Verify parameters
        assert "api_key" in call_kwargs
        assert "model" in call_kwargs
        assert "temperature" in call_kwargs
        assert 0.0 <= call_kwargs["temperature"] <= 2.0  # Valid temperature range

        # Verify invoke was called
        mock_llm.invoke.assert_called_once()

        # Verify output
        captured = capsys.readouterr()
        assert "OpenAI" in captured.out
        assert "Machine learning is a subset of AI" in captured.out

    def test_basic_openai_uses_configured_model(self, mock_env_vars, monkeypatch):
        """
        Test that configured model is used when available.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        """
        # Set model configuration
        monkeypatch.setenv("EADLANGCHAIN_AI_OPENAI_MODEL", "gpt-4o")

        # Reload module to pick up env var
        importlib.reload(basic_01)

        # Create mock
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Test")
        mock_chat_class = Mock(return_value=mock_llm)
        monkeypatch.setattr(basic_01, "ChatOpenAI", mock_chat_class)

        # Run
        basic_01.basic_openai_example()

        # Verify configured model was used
        call_kwargs = mock_chat_class.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o"

    def test_main_handles_provider_failures(self, mock_env_vars, monkeypatch, capsys):
        """
        Test that main() catches and reports errors from individual providers.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        # Mock providers to simulate failures
        def failing_openai():
            """Mock function that simulates OpenAI failure."""
            raise Exception("OpenAI API error")

        def failing_anthropic():
            """Mock function that simulates Anthropic failure."""
            raise Exception("Anthropic API error")

        def succeeding_gemini():
            """Mock function that simulates successful Gemini call."""
            pass

        monkeypatch.setattr(basic_01, "basic_openai_example", failing_openai)
        monkeypatch.setattr(basic_01, "basic_anthropic_example", failing_anthropic)
        monkeypatch.setattr(basic_01, "basic_gemini_example", succeeding_gemini)

        # Run main - should not crash
        basic_01.main()

        # Verify errors were reported
        captured = capsys.readouterr()
        assert "[ERROR]" in captured.out
        assert "OpenAI" in captured.out or "Anthropic" in captured.out
        assert "[SUCCESS] Basic examples complete!" in captured.out


class TestStreamingExamples:
    """Tests for 02_streaming.py functionality."""

    def test_streaming_module_has_required_functions(self):
        """
        Test that streaming module exports expected functions.

        :return: None
        :rtype: None
        """
        assert hasattr(streaming_02, "streaming_openai_example")
        assert hasattr(streaming_02, "streaming_anthropic_example")
        assert hasattr(streaming_02, "streaming_gemini_example")
        assert hasattr(streaming_02, "advanced_streaming_example")
        assert hasattr(streaming_02, "main")

    def test_streaming_example_uses_stream_method(self, mock_env_vars, monkeypatch, capsys):
        """
        Test that streaming examples use stream() method.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        # Create mock LLM with streaming support
        mock_llm = Mock()
        mock_chunks = [
            Mock(content="Streaming "),
            Mock(content="allows "),
            Mock(content="real-time "),
            Mock(content="responses."),
        ]
        mock_llm.stream.return_value = iter(mock_chunks)

        mock_chat_class = Mock(return_value=mock_llm)
        monkeypatch.setattr(streaming_02, "ChatOpenAI", mock_chat_class)

        # Run streaming example
        streaming_02.streaming_openai_example()

        # Verify stream was called
        mock_llm.stream.assert_called_once()

        # Verify output was streamed
        captured = capsys.readouterr()
        assert "Streaming allows real-time responses" in captured.out

    def test_advanced_streaming_collects_chunks(self, mock_env_vars, monkeypatch, capsys):
        """
        Test that advanced streaming collects chunks.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_chunks = [Mock(content="Line "), Mock(content="by "), Mock(content="line")]
        mock_llm.stream.return_value = iter(mock_chunks)

        mock_chat_class = Mock(return_value=mock_llm)
        monkeypatch.setattr(streaming_02, "ChatOpenAI", mock_chat_class)

        streaming_02.advanced_streaming_example()

        captured = capsys.readouterr()
        assert "Received 3 chunks" in captured.out


class TestConversationExamples:
    """Tests for 03_conversation.py functionality."""

    def test_conversation_module_has_required_functions(self):
        """
        Test that conversation module exports expected functions.

        :return: None
        :rtype: None
        """
        assert hasattr(conversation_03, "basic_conversation_example")
        assert hasattr(conversation_03, "interactive_conversation_example")
        assert hasattr(conversation_03, "multi_provider_conversation")
        assert hasattr(conversation_03, "main")

    def test_basic_conversation_maintains_history(self, mock_env_vars, monkeypatch, capsys):
        """
        Test that conversation maintains message history.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        # Three responses for three conversation turns
        mock_llm.invoke.side_effect = [
            Mock(content="Machine learning is a subset of AI."),
            Mock(content="Sure! Spam detection is a common example."),
            Mock(content="Your first question was about machine learning."),
        ]

        mock_chat_class = Mock(return_value=mock_llm)
        monkeypatch.setattr(conversation_03, "ChatOpenAI", mock_chat_class)

        conversation_03.basic_conversation_example()

        # Verify invoke was called three times (one per turn)
        assert mock_llm.invoke.call_count == 3

        # Verify conversation happened by checking output
        captured = capsys.readouterr()
        assert "Total messages in history" in captured.out
        assert "7" in captured.out  # Should have 7 messages total


class TestAdvancedExamples:
    """Tests for 04_advanced.py functionality."""

    def test_advanced_module_has_required_functions(self):
        """
        Test that advanced module exports expected functions.

        :return: None
        :rtype: None
        """
        assert hasattr(advanced_04, "token_tracking_example")
        assert hasattr(advanced_04, "metadata_inspection_example")
        assert hasattr(advanced_04, "retry_and_error_handling_example")
        assert hasattr(advanced_04, "batch_processing_example")
        assert hasattr(advanced_04, "advanced_parameters_example")
        assert hasattr(advanced_04, "main")

    def test_advanced_module_has_callback_class(self):
        """
        Test that TokenCounterCallback is defined.

        :return: None
        :rtype: None
        """
        assert hasattr(advanced_04, "TokenCounterCallback")
        assert callable(advanced_04.TokenCounterCallback)

    def test_token_counter_callback_tracks_usage(self):
        """
        Test that TokenCounterCallback tracks token usage.

        :return: None
        :rtype: None
        """
        callback = advanced_04.TokenCounterCallback()

        # Simulate LLM end event
        mock_response = Mock()
        mock_response.llm_output = {
            "token_usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            "model_name": "gpt-5-nano",
        }

        callback.on_llm_end(mock_response)

        summary = callback.get_summary()
        assert summary["total_tokens"] == 30
        assert summary["prompt_tokens"] == 10
        assert summary["completion_tokens"] == 20

    def test_batch_processing_uses_batch_method(self, mock_env_vars, monkeypatch, capsys):
        """
        Test that batch processing uses batch() method.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        # Mock batch returns responses (not wrapped in lists)
        mock_llm.batch.return_value = [
            Mock(content="Python is a programming language."),
            Mock(content="JavaScript runs in browsers."),
            Mock(content="Rust is memory-safe."),
        ]

        mock_chat_class = Mock(return_value=mock_llm)
        monkeypatch.setattr(advanced_04, "ChatOpenAI", mock_chat_class)

        advanced_04.batch_processing_example()

        # Verify batch was called
        mock_llm.batch.assert_called_once()

        captured = capsys.readouterr()
        assert "Batch Processing" in captured.out


class TestBasicExampleAllProviders:
    """Test all providers in 01_basic.py."""

    def test_anthropic_example_works(self, mock_env_vars, monkeypatch, capsys):
        """
        Test Anthropic example runs correctly.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Claude response")
        monkeypatch.setattr(basic_01, "ChatAnthropic", Mock(return_value=mock_llm))

        basic_01.basic_anthropic_example()

        captured = capsys.readouterr()
        assert "Anthropic" in captured.out
        assert "Claude response" in captured.out

    def test_gemini_example_works(self, mock_env_vars, monkeypatch, capsys):
        """
        Test Gemini example runs correctly.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Gemini response")
        monkeypatch.setattr(basic_01, "ChatGoogleGenerativeAI", Mock(return_value=mock_llm))

        basic_01.basic_gemini_example()

        captured = capsys.readouterr()
        assert "Gemini" in captured.out
        assert "Gemini response" in captured.out


class TestStreamingAllProviders:
    """Test all providers in 02_streaming.py."""

    def test_anthropic_streaming_works(self, mock_env_vars, monkeypatch, capsys):
        """
        Test Anthropic streaming example.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.stream.return_value = iter([Mock(content="Claude "), Mock(content="streams")])
        monkeypatch.setattr(streaming_02, "ChatAnthropic", Mock(return_value=mock_llm))

        streaming_02.streaming_anthropic_example()

        captured = capsys.readouterr()
        assert "Claude streams" in captured.out

    def test_gemini_streaming_works(self, mock_env_vars, monkeypatch, capsys):
        """
        Test Gemini streaming example.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.stream.return_value = iter([Mock(content="Gemini "), Mock(content="streams")])
        monkeypatch.setattr(streaming_02, "ChatGoogleGenerativeAI", Mock(return_value=mock_llm))

        streaming_02.streaming_gemini_example()

        captured = capsys.readouterr()
        assert "Gemini streams" in captured.out

    def test_streaming_main_runs_all(self, mock_env_vars, monkeypatch, capsys):
        """
        Test streaming main function.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        # Mock all three providers
        mock_llm = Mock()
        mock_llm.stream.return_value = iter([Mock(content="test")])
        monkeypatch.setattr(streaming_02, "ChatOpenAI", Mock(return_value=mock_llm))
        monkeypatch.setattr(streaming_02, "ChatAnthropic", Mock(return_value=mock_llm))
        monkeypatch.setattr(streaming_02, "ChatGoogleGenerativeAI", Mock(return_value=mock_llm))

        streaming_02.main()

        captured = capsys.readouterr()
        assert "Example 02" in captured.out


class TestConversationAllExamples:
    """Test all conversation examples in 03_conversation.py."""

    def test_interactive_conversation_example(self, mock_env_vars, monkeypatch, capsys):
        """
        Test interactive conversation helper.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        # Need more responses for the helper function iterations
        mock_llm.invoke.side_effect = [
            Mock(content="Python is a language."),
            Mock(content="Yes, it is."),
            Mock(content="Great question."),
        ]
        monkeypatch.setattr(conversation_03, "ChatAnthropic", Mock(return_value=mock_llm))

        conversation_03.interactive_conversation_example()

        assert mock_llm.invoke.call_count >= 2
        captured = capsys.readouterr()
        assert "Interactive Conversation" in captured.out

    def test_multi_provider_conversation(self, mock_env_vars, monkeypatch, capsys):
        """
        Test multi-provider conversation comparison.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Provider response")

        monkeypatch.setattr(conversation_03, "ChatOpenAI", Mock(return_value=mock_llm))
        monkeypatch.setattr(conversation_03, "ChatAnthropic", Mock(return_value=mock_llm))
        monkeypatch.setattr(conversation_03, "ChatGoogleGenerativeAI", Mock(return_value=mock_llm))

        conversation_03.multi_provider_conversation()

        captured = capsys.readouterr()
        assert "Multi-Provider" in captured.out

    def test_conversation_main(self, mock_env_vars, monkeypatch, capsys):
        """
        Test conversation main function.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Test response")

        monkeypatch.setattr(conversation_03, "ChatOpenAI", Mock(return_value=mock_llm))
        monkeypatch.setattr(conversation_03, "ChatAnthropic", Mock(return_value=mock_llm))
        monkeypatch.setattr(conversation_03, "ChatGoogleGenerativeAI", Mock(return_value=mock_llm))

        conversation_03.main()

        captured = capsys.readouterr()
        assert "Example 03" in captured.out


class TestAdvancedAllExamples:
    """Test all advanced examples in 04_advanced.py."""

    def test_token_tracking_actually_runs(self, mock_env_vars, monkeypatch, capsys):
        """
        Test token tracking example execution.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Response")

        monkeypatch.setattr(advanced_04, "ChatOpenAI", Mock(return_value=mock_llm))

        advanced_04.token_tracking_example()

        assert mock_llm.invoke.call_count >= 3
        captured = capsys.readouterr()
        assert "Token Tracking" in captured.out

    def test_metadata_inspection_runs(self, mock_env_vars, monkeypatch, capsys):
        """
        Test metadata inspection example.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "Metadata explanation"
        mock_response.response_metadata = {"model": "test-model"}
        mock_llm.invoke.return_value = mock_response

        monkeypatch.setattr(advanced_04, "ChatAnthropic", Mock(return_value=mock_llm))

        advanced_04.metadata_inspection_example()

        captured = capsys.readouterr()
        assert "Metadata" in captured.out

    def test_retry_example_runs(self, mock_env_vars, monkeypatch, capsys):
        """
        Test retry and error handling example.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Success response")

        monkeypatch.setattr(advanced_04, "ChatOpenAI", Mock(return_value=mock_llm))

        advanced_04.retry_and_error_handling_example()

        captured = capsys.readouterr()
        assert "Error Handling" in captured.out or "Retry" in captured.out

    def test_advanced_parameters_example(self, mock_env_vars, monkeypatch, capsys):
        """
        Test advanced parameters example.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Parameter response")

        monkeypatch.setattr(advanced_04, "ChatOpenAI", Mock(return_value=mock_llm))

        advanced_04.advanced_parameters_example()

        # Should be called multiple times for different token limits
        assert mock_llm.invoke.call_count >= 2

    def test_advanced_main(self, mock_env_vars, monkeypatch, capsys):
        """
        Test advanced main function.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Test")
        mock_llm.batch.return_value = [[Mock(content="Batch result")]]

        monkeypatch.setattr(advanced_04, "ChatOpenAI", Mock(return_value=mock_llm))
        monkeypatch.setattr(advanced_04, "ChatAnthropic", Mock(return_value=mock_llm))

        advanced_04.main()

        captured = capsys.readouterr()
        assert "Example 04" in captured.out


class TestExampleCoverage:
    """Integration tests ensuring examples work end-to-end."""

    def test_all_main_functions_are_callable(self):
        """
        Test that all example modules have callable main functions.

        :return: None
        :rtype: None
        """
        assert callable(basic_01.main)
        assert callable(streaming_02.main)
        assert callable(conversation_03.main)
        assert callable(advanced_04.main)

    def test_examples_use_get_model_name(self):
        """
        Test that examples import and can use get_model_name.

        :return: None
        :rtype: None
        """
        # Verify all examples imported get_model_name
        assert hasattr(basic_01, "get_model_name")
        assert hasattr(streaming_02, "get_model_name")
        assert hasattr(conversation_03, "get_model_name")
        assert hasattr(advanced_04, "get_model_name")

    def test_basic_main_executes(self, mock_env_vars, monkeypatch, capsys):
        """
        Test basic main function executes successfully.

        :param mock_env_vars: Pytest fixture providing mocked environment variables
        :ptype mock_env_vars: None
        :param monkeypatch: Pytest fixture for modifying environment
        :ptype monkeypatch: pytest.MonkeyPatch
        :param capsys: Pytest fixture for capturing output
        :ptype capsys: CaptureFixture
        """
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="Test")

        monkeypatch.setattr(basic_01, "ChatOpenAI", Mock(return_value=mock_llm))
        monkeypatch.setattr(basic_01, "ChatAnthropic", Mock(return_value=mock_llm))
        monkeypatch.setattr(basic_01, "ChatGoogleGenerativeAI", Mock(return_value=mock_llm))

        basic_01.main()

        captured = capsys.readouterr()
        assert "Basic examples complete" in captured.out
