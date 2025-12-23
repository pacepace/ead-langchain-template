"""
Example 01: Basic LLM Usage

This example demonstrates the simplest possible way to use LangChain with
different providers. Just prompt → response, no complexity.

Shows:
- Loading configuration
- Basic invocation with OpenAI, Anthropic, and Gemini
"""

# Third-party imports
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Local imports
from langchain_llm import get_api_key, get_logger, get_model_name, load_env_config, setup_logging

# Setup logging and configuration
setup_logging()
logger = get_logger(__name__)
load_env_config()


def basic_openai_example():
    """Simple example using OpenAI."""
    logger.info("Running OpenAI basic example")

    # Get API key and model name using our custom config
    api_key = get_api_key("openai")
    # Use configured model or fall back to cost-effective default
    # Configure via EADLANGCHAIN_AI_OPENAI_MODEL in .env
    model_name = get_model_name("openai") or "gpt-5-nano"

    # Create LangChain ChatOpenAI instance
    # Default: gpt-5-nano (most cost-effective: $0.05/$0.40 per million tokens)
    # For better quality, try: gpt-5, gpt-5-mini, gpt-4o
    # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=1.0,  # Required for gpt-5-nano/gpt-5-mini/gpt-5
        # For gpt-5-chat-latest or gpt-4o models, you can use custom temperature:
        # temperature=0.7,  # Use this with gpt-5-chat-latest or gpt-4o
    )

    # Simple invoke - just send a message and get a response
    response = llm.invoke("What is machine learning in one sentence?")

    print(f"\n{'=' * 80}")
    print("OpenAI (gpt-5-nano):")
    print(f"{'=' * 80}")
    print(response.content)
    print()


def basic_anthropic_example():
    """Simple example using Anthropic Claude."""
    logger.info("Running Anthropic basic example")

    # Get API key and model name using our custom config
    api_key = get_api_key("anthropic")
    # Use configured model or fall back to cost-effective default
    model_name = get_model_name("anthropic") or "claude-3-haiku-20240307"

    # Create LangChain ChatAnthropic instance
    # Default: claude-3-haiku-20240307 (most cost-effective Claude 3 model)
    # For better quality, try: claude-3-5-sonnet-20241022, claude-haiku-4-5
    llm = ChatAnthropic(
        model=model_name,
        api_key=api_key,
        temperature=0.7,
    )

    # Simple invoke - just send a message and get a response
    response = llm.invoke("What is machine learning in one sentence?")

    print(f"\n{'=' * 80}")
    print("Anthropic (Claude 3 Haiku):")
    print(f"{'=' * 80}")
    print(response.content)
    print()


def basic_gemini_example():
    """Simple example using Google Gemini."""
    logger.info("Running Gemini basic example")

    # Get API key and model name using our custom config
    api_key = get_api_key("gemini")
    # Use configured model or fall back to cost-effective default
    model_name = get_model_name("gemini") or "gemini-2.0-flash-lite"

    # Create LangChain ChatGoogleGenerativeAI instance
    # Default: gemini-2.0-flash-lite (most cost-effective: $0.07/$0.30 per million tokens)
    # For better quality, try: gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-pro
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.7,
    )

    # Simple invoke - just send a message and get a response
    response = llm.invoke("What is machine learning in one sentence?")

    print(f"\n{'=' * 80}")
    print("Google Gemini (2.0 Flash-Lite):")
    print(f"{'=' * 80}")
    print(response.content)
    print()


def main():
    """Run all basic examples."""
    print("\n" + "=" * 80)
    print("Example 01: Basic LLM Usage")
    print("=" * 80)
    print("\nThis example shows the simplest way to use LangChain with different providers.")
    print("Notice how similar the code is for each provider - that's the power of LangChain!")
    print()

    # Run examples for each provider
    # Comment out providers you don't have API keys for
    try:
        basic_openai_example()
    except Exception as e:
        logger.error(f"OpenAI example failed: {e}")
        print(f"[ERROR] OpenAI example failed ({type(e).__name__}): {e}\n")

    try:
        basic_anthropic_example()
    except Exception as e:
        logger.error(f"Anthropic example failed: {e}")
        print(f"[ERROR] Anthropic example failed ({type(e).__name__}): {e}\n")

    try:
        basic_gemini_example()
    except Exception as e:
        logger.error(f"Gemini example failed: {e}")
        print(f"[ERROR] Gemini example failed ({type(e).__name__}): {e}\n")

    print("=" * 80)
    print("[SUCCESS] Basic examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
