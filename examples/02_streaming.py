"""
Example 02: Streaming Responses

This example demonstrates how to stream LLM responses token by token.
Streaming is useful for:
- Providing real-time feedback to users
- Building interactive chat applications
- Reducing perceived latency

Shows:
- Basic streaming with .stream()
- Handling streaming responses
- Streaming with different providers
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


def streaming_openai_example():
    """Stream responses from OpenAI."""
    logger.info("Running OpenAI streaming example")

    api_key = get_api_key("openai")
    model_name = get_model_name("openai") or "gpt-5-nano"
    # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=1.0,
    )

    print(f"\n{'=' * 80}")
    print("OpenAI Streaming (gpt-5-nano):")
    print(f"{'=' * 80}")
    print()

    # Stream the response - each chunk arrives as it's generated
    for chunk in llm.stream("Explain the history of artificial intelligence in 3 paragraphs"):
        # chunk.content contains the new text
        print(chunk.content, end="", flush=True)

    print("\n")


def streaming_anthropic_example():
    """Stream responses from Anthropic Claude."""
    logger.info("Running Anthropic streaming example")

    api_key = get_api_key("anthropic")
    model_name = get_model_name("anthropic") or "claude-3-haiku-20240307"
    llm = ChatAnthropic(
        model=model_name,
        api_key=api_key,
        temperature=0.7,
    )

    print(f"\n{'=' * 80}")
    print("Anthropic Streaming (Claude 3 Haiku):")
    print(f"{'=' * 80}")
    print()

    # Stream the response
    for chunk in llm.stream("Explain the history of artificial intelligence in 3 paragraphs"):
        print(chunk.content, end="", flush=True)

    print("\n")


def streaming_gemini_example():
    """Stream responses from Google Gemini."""
    logger.info("Running Gemini streaming example")

    api_key = get_api_key("gemini")
    model_name = get_model_name("gemini") or "gemini-2.0-flash-lite"
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.7,
    )

    print(f"\n{'=' * 80}")
    print("Google Gemini Streaming (2.0 Flash-Lite):")
    print(f"{'=' * 80}")
    print()

    # Stream the response
    for chunk in llm.stream("Explain the history of artificial intelligence in 3 paragraphs"):
        print(chunk.content, end="", flush=True)

    print("\n")


def advanced_streaming_example():
    """
    More advanced streaming example showing how to:
    - Collect chunks for later processing
    - Track streaming progress
    """
    logger.info("Running advanced streaming example")

    api_key = get_api_key("openai")
    # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
    llm = ChatOpenAI(model=get_model_name("openai") or "gpt-5-nano", api_key=api_key, temperature=1.0)

    print(f"\n{'=' * 80}")
    print("Advanced Streaming Example:")
    print(f"{'=' * 80}")
    print()
    print("Prompt: Write a haiku about AI")
    print("\nResponse:")
    print("-" * 40)

    # Collect chunks while streaming
    full_response = ""
    chunk_count = 0

    for chunk in llm.stream("Write a haiku about AI"):
        content = chunk.content
        full_response += content
        chunk_count += 1
        print(content, end="", flush=True)

    print()
    print("-" * 40)
    print(f"\nReceived {chunk_count} chunks")
    print(f"Total characters: {len(full_response)}")
    print()


def main():
    """Run all streaming examples."""
    print("\n" + "=" * 80)
    print("Example 02: Streaming Responses")
    print("=" * 80)
    print("\nStreaming allows you to see responses as they're generated,")
    print("token by token, instead of waiting for the complete response.")
    print("\nWatch the text appear in real-time!")
    print()

    # Run examples for each provider
    try:
        streaming_openai_example()
    except Exception as e:
        logger.error(f"OpenAI streaming example failed: {e}")
        print(f"[ERROR] OpenAI example failed ({type(e).__name__}): {e}\n")

    try:
        streaming_anthropic_example()
    except Exception as e:
        logger.error(f"Anthropic streaming example failed: {e}")
        print(f"[ERROR] Anthropic example failed ({type(e).__name__}): {e}\n")

    try:
        streaming_gemini_example()
    except Exception as e:
        logger.error(f"Gemini streaming example failed: {e}")
        print(f"[ERROR] Gemini example failed ({type(e).__name__}): {e}\n")

    try:
        advanced_streaming_example()
    except Exception as e:
        logger.error(f"Advanced streaming example failed: {e}")
        print(f"[ERROR] Advanced example failed ({type(e).__name__}): {e}\n")

    print("=" * 80)
    print("[SUCCESS] Streaming examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
