"""
Example 04: Advanced Features

This example demonstrates advanced LangChain features for production use:
- Token counting and cost tracking with callbacks
- Response metadata inspection
- Error handling and retries
- Batch processing
- Model parameters tuning

These features are optional but useful when building production applications.

Using most cost-effective models as of October 2025:
  gpt-5-nano, claude-3-haiku-20240307, gemini-2.0-flash-lite
"""

# Standard library imports
import time

# Third-party imports
from langchain_anthropic import ChatAnthropic
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_openai import ChatOpenAI

# Local imports
from langchain_llm import get_api_key, get_logger, get_model_name, load_env_config, setup_logging

# Set up logging and configuration
setup_logging()
logger = get_logger(__name__)
load_env_config()


class TokenCounterCallback(BaseCallbackHandler):
    """
    Custom callback to track token usage and estimate costs.

    LangChain callbacks allow you to hook into LLM lifecycle
    and track metrics like tokens, latency, and costs.
    """

    def __init__(self):
        """
        Initialize token tracker.
        """
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_cost = 0.0

        # Approximate pricing (as of October 2025 - check current pricing!)
        self.pricing = {
            "gpt-5-nano": {"prompt": 0.05 / 1000, "completion": 0.40 / 1000},
            "claude-3-haiku-20240307": {"prompt": 0.25 / 1000, "completion": 1.25 / 1000},
            "gemini-2.0-flash-lite": {"prompt": 0.07 / 1000, "completion": 0.30 / 1000},
        }

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """
        Called when LLM finishes running.

        :param response: LLM result containing outputs and metadata
        :ptype response: LLMResult
        :param kwargs: Additional keyword arguments
        :return: None
        :rtype: None
        """
        # Extract token usage from response metadata
        if response.llm_output and "token_usage" in response.llm_output:
            usage = response.llm_output["token_usage"]
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)

            self.prompt_tokens += prompt_tokens
            self.completion_tokens += completion_tokens
            self.total_tokens += total_tokens

            # Estimate cost (if model is known)
            model = response.llm_output.get("model_name", "")
            if model in self.pricing:
                cost = (prompt_tokens * self.pricing[model]["prompt"]) + (completion_tokens * self.pricing[model]["completion"])
                self.total_cost += cost

    def get_summary(self) -> dict[str, int | float]:
        """
        Get summary of token usage and costs.

        :return: Dictionary with token counts and estimated cost
        :rtype: dict[str, int | float]
        """
        return {
            "total_tokens": self.total_tokens,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "estimated_cost_usd": round(self.total_cost, 6),
        }


def token_tracking_example():
    """
    Demonstrate token counting and cost tracking using callbacks.
    """
    logger.info("Running token tracking example")

    print(f"\n{'=' * 80}")
    print("Token Tracking & Cost Estimation")
    print(f"{'=' * 80}\n")

    api_key = get_api_key("openai")

    # Create callback instance
    token_counter = TokenCounterCallback()

    # Pass callbacks to the LLM
    # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
    llm = ChatOpenAI(
        model=get_model_name("openai") or "gpt-5-nano",
        api_key=api_key,
        temperature=1.0,
        callbacks=[token_counter],  # Attach our callback
    )

    # Make several calls
    prompts = [
        "What is machine learning?",
        "Explain neural networks in one sentence.",
        "What is the difference between AI and ML?",
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"Query {i}: {prompt}")
        response = llm.invoke(prompt)
        print(f"Response: {response.content[:100]}...\n")

    # Get usage summary
    summary = token_counter.get_summary()
    print("-" * 80)
    print("Token Usage Summary:")
    print(f"  Total tokens: {summary['total_tokens']}")
    print(f"  Prompt tokens: {summary['prompt_tokens']}")
    print(f"  Completion tokens: {summary['completion_tokens']}")
    print(f"  Estimated cost: ${summary['estimated_cost_usd']:.6f}")
    print()


def metadata_inspection_example():
    """
    Inspect response metadata to understand model behavior.
    """
    logger.info("Running metadata inspection example")

    print(f"\n{'=' * 80}")
    print("Response Metadata Inspection")
    print(f"{'=' * 80}\n")

    api_key = get_api_key("anthropic")
    llm = ChatAnthropic(model=get_model_name("anthropic") or "claude-3-haiku-20240307", api_key=api_key, temperature=0.7)

    # Get response with metadata
    response = llm.invoke("Explain what metadata is in one sentence.")

    print(f"Response: {response.content}\n")
    print("Response Metadata:")
    print(f"  Model: {response.response_metadata.get('model', 'N/A')}")
    print(f"  Stop reason: {response.response_metadata.get('stop_reason', 'N/A')}")

    # Token usage (if available)
    usage = response.response_metadata.get("usage", {})
    if usage:
        print(f"  Input tokens: {usage.get('input_tokens', 'N/A')}")
        print(f"  Output tokens: {usage.get('output_tokens', 'N/A')}")

    # Additional fields vary by provider
    print(f"  Additional metadata: {list(response.response_metadata.keys())}")
    print()


def retry_and_error_handling_example():
    """
    Demonstrate error handling and retry patterns.
    """
    logger.info("Running retry and error handling example")

    print(f"\n{'=' * 80}")
    print("Error Handling & Retry Logic")
    print(f"{'=' * 80}\n")

    api_key = get_api_key("openai")
    # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
    llm = ChatOpenAI(
        model=get_model_name("openai") or "gpt-5-nano",
        api_key=api_key,
        temperature=1.0,
        max_retries=3,  # LangChain has built-in retry logic!
        request_timeout=30,  # Timeout after 30 seconds
    )

    # Example: Handling failures gracefully
    prompts = ["What is Python?", "Explain JavaScript briefly."]

    for prompt in prompts:
        try:
            print(f"Query: {prompt}")
            response = llm.invoke(prompt)
            print(f"[SUCCESS] Response: {response.content[:80]}...\n")
        except Exception as e:
            logger.error(f"Failed to get response: {e}")
            print(f"[ERROR] Error: {e}\n")


def batch_processing_example():
    """
    Process multiple prompts using LangChain's batch method.

    Note: LangChain's batch() makes separate API calls (potentially in parallel)
    for each prompt. This is different from API-level batching which would
    send all prompts in a single request. The benefit is convenience and
    potential parallelization, not reduced API calls.
    """
    logger.info("Running batch processing example")

    print(f"\n{'=' * 80}")
    print("Batch Processing")
    print(f"{'=' * 80}\n")

    api_key = get_api_key("openai")
    # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
    llm = ChatOpenAI(model=get_model_name("openai") or "gpt-5-nano", api_key=api_key, temperature=1.0)

    # Multiple prompts to process
    prompts = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?",
    ]

    print("Processing 3 prompts in batch...\n")
    start_time = time.time()

    # LangChain's batch() method processes multiple prompts
    # Makes separate API calls (one per prompt) but provides convenient interface
    # Pass strings directly - LangChain wraps them in messages internally
    responses = llm.batch(prompts)

    elapsed = time.time() - start_time

    for prompt, response in zip(prompts, responses):
        print(f"Q: {prompt}")
        print(f"A: {response.content[:80]}...\n")

    print(f"Processed {len(prompts)} prompts in {elapsed:.2f} seconds")
    print()


def advanced_parameters_example():
    """
    Demonstrate advanced model parameters for fine-tuning behavior.

    NOTE: GPT-5 models (gpt-5-nano, gpt-5-mini, gpt-5) have limited parameter support.
    They only support temperature=1.0 and do not support top_p or other tuning parameters.
    Use gpt-5-chat-latest or gpt-4o models for full parameter control.
    """
    logger.info("Running advanced parameters example")

    print(f"\n{'=' * 80}")
    print("Advanced Model Parameters")
    print(f"{'=' * 80}\n")

    api_key = get_api_key("openai")

    # GPT-5 models support max_tokens but not temperature/top_p variations
    # Demonstrating max_tokens to control response length
    token_limits = [20, 50]
    prompt = "Write a creative opening line for a sci-fi story."

    for max_tok in token_limits:
        llm = ChatOpenAI(
            model=get_model_name("openai") or "gpt-5-nano",
            api_key=api_key,
            temperature=1.0,  # GPT-5 requires temperature=1
            max_tokens=max_tok,  # Limit response length
        )

        response = llm.invoke(prompt)
        print(f"Max tokens: {max_tok}")
        print(f"  {response.content}\n")

    # For full parameter control, use gpt-5-chat-latest or gpt-4o:
    # llm = ChatOpenAI(
    #     model="gpt-5-chat-latest",  # or "gpt-4o"
    #     api_key=api_key,
    #     temperature=0.7,  # Custom temperature supported
    #     top_p=0.9,  # Nucleus sampling supported
    #     max_tokens=100,
    # )


def main():
    """Run all advanced examples."""
    print("\n" + "=" * 80)
    print("Example 04: Advanced Features")
    print("=" * 80)
    print("\nThese examples show advanced features for production applications.")
    print("Start simple (examples 01-03) and add these features as needed.")
    print()

    try:
        token_tracking_example()
    except Exception as e:
        logger.error(f"Token tracking example failed: {type(e).__name__}: {e}")
        print(f"[ERROR] Token tracking example failed ({type(e).__name__}): {e}\n")

    try:
        metadata_inspection_example()
    except Exception as e:
        logger.error(f"Metadata inspection example failed: {type(e).__name__}: {e}")
        print(f"[ERROR] Metadata inspection example failed ({type(e).__name__}): {e}\n")

    try:
        retry_and_error_handling_example()
    except Exception as e:
        logger.error(f"Retry example failed: {type(e).__name__}: {e}")
        print(f"[ERROR] Retry example failed ({type(e).__name__}): {e}\n")

    try:
        batch_processing_example()
    except Exception as e:
        logger.error(f"Batch processing example failed: {type(e).__name__}: {e}")
        print(f"[ERROR] Batch processing example failed ({type(e).__name__}): {e}\n")

    try:
        advanced_parameters_example()
    except Exception as e:
        logger.error(f"Advanced parameters example failed: {type(e).__name__}: {e}")
        print(f"[ERROR] Advanced parameters example failed ({type(e).__name__}): {e}\n")

    print("=" * 80)
    print("[SUCCESS] Advanced examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
