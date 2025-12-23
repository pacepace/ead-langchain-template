"""
Example 03: Conversations with Message History

This example demonstrates how to maintain conversation history for
multi-turn interactions with LLMs.

Shows:
- Managing message history
- Multi-turn conversations
- Different message types (system, human, AI)
- Conversation with different providers
"""

# Third-party imports
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Local imports
from langchain_llm import get_api_key, get_logger, get_model_name, load_env_config, setup_logging

# Setup logging and configuration
setup_logging()
logger = get_logger(__name__)
load_env_config()


def basic_conversation_example():
    """
    Basic conversation with message history.
    Shows how to manually manage conversation.
    """
    logger.info("Running basic conversation example")

    api_key = get_api_key("openai")
    model_name = get_model_name("openai") or "gpt-5-nano"
    # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
    llm = ChatOpenAI(model=model_name, api_key=api_key, temperature=1.0)

    print(f"\n{'=' * 80}")
    print("Basic Conversation Example (OpenAI)")
    print(f"{'=' * 80}\n")

    # Initialize conversation history
    # SystemMessage sets the behavior/context
    # HumanMessage represents user input
    # AIMessage represents assistant responses
    conversation_history = [
        SystemMessage(content="You are a helpful AI assistant that specializes in explaining technical concepts simply."),
    ]

    # First turn
    print("Human: What is machine learning?")
    conversation_history.append(HumanMessage(content="What is machine learning?"))

    response = llm.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.content))

    print(f"AI: {response.content}\n")

    # Second turn - AI remembers context
    print("Human: Can you give me a simple example?")
    conversation_history.append(HumanMessage(content="Can you give me a simple example?"))

    response = llm.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.content))

    print(f"AI: {response.content}\n")

    # Third turn - testing memory
    print("Human: What was my first question?")
    conversation_history.append(HumanMessage(content="What was my first question?"))

    response = llm.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.content))

    print(f"AI: {response.content}\n")

    print(f"Total messages in history: {len(conversation_history)}")


def interactive_conversation_example():
    """
    Interactive conversation helper function.
    You can use this pattern to build chat applications.
    """
    logger.info("Running interactive conversation example")

    api_key = get_api_key("anthropic")
    model_name = get_model_name("anthropic") or "claude-3-haiku-20240307"
    llm = ChatAnthropic(model=model_name, api_key=api_key, temperature=0.7)

    print(f"\n{'=' * 80}")
    print("Interactive Conversation Helper (Anthropic)")
    print(f"{'=' * 80}\n")

    # Define a reusable conversation function
    def have_conversation(llm_instance, system_prompt: str, turns: list[str]):
        """
        Helper function to have multi-turn conversation.

        :param llm_instance: LangChain LLM instance
        :ptype llm_instance: ChatOpenAI | ChatAnthropic | ChatGoogleGenerativeAI
        :param system_prompt: Initial system prompt
        :ptype system_prompt: str
        :param turns: list of user messages
        :ptype turns: list[str]
        :return: List of (human_msg, ai_response) tuples
        :rtype: list
        """
        history = [SystemMessage(content=system_prompt)]
        conversation = []

        for user_message in turns:
            history.append(HumanMessage(content=user_message))
            response = llm_instance.invoke(history)
            history.append(AIMessage(content=response.content))
            conversation.append((user_message, response.content))

        return conversation

    # Use the helper
    conversation = have_conversation(
        llm,
        system_prompt="You are a creative writing assistant.",
        turns=[
            "Help me start a story about a robot.",
            "What should happen next?",
            "Give me a twist ending.",
        ],
    )

    # Display the conversation
    for i, (human, ai) in enumerate(conversation, 1):
        print(f"Turn {i}:")
        print(f"  Human: {human}")
        print(f"  AI: {ai[:200]}{'...' if len(ai) > 200 else ''}\n")


def multi_provider_conversation():
    """
    Example showing how conversation works same across providers.
    """
    logger.info("Running multi-provider conversation example")

    print(f"\n{'=' * 80}")
    print("Multi-Provider Conversation Comparison")
    print(f"{'=' * 80}\n")

    # Set up all three providers
    providers = []

    try:
        openai_key = get_api_key("openai")
        openai_model = get_model_name("openai") or "gpt-5-nano"
        # NOTE: GPT-5 models require temperature=1 (except gpt-5-chat-latest which supports other values)
        providers.append(("OpenAI", ChatOpenAI(model=openai_model, api_key=openai_key, temperature=1.0)))
    except Exception as e:
        print(f"[WARNING] OpenAI not available: {e}")

    try:
        anthropic_key = get_api_key("anthropic")
        anthropic_model = get_model_name("anthropic") or "claude-3-haiku-20240307"
        providers.append(("Anthropic", ChatAnthropic(model=anthropic_model, api_key=anthropic_key, temperature=0.7)))
    except Exception as e:
        print(f"[WARNING] Anthropic not available: {e}")

    try:
        gemini_key = get_api_key("gemini")
        gemini_model = get_model_name("gemini") or "gemini-2.0-flash-lite"
        providers.append(
            ("Gemini", ChatGoogleGenerativeAI(model=gemini_model, google_api_key=gemini_key, temperature=0.7))
        )
    except Exception as e:
        print(f"[WARNING] Gemini not available: {e}")

    if not providers:
        print("[WARNING] No providers available. Please configure at least one API key.\n")
        return

    # Same conversation with all providers
    conversation_history = [
        SystemMessage(content="You are a math tutor."),
        HumanMessage(content="What is 15 * 24?"),
    ]

    for provider_name, llm in providers:
        print(f"\n{provider_name} Response:")
        print("-" * 60)
        response = llm.invoke(conversation_history)
        print(response.content[:200] + ("..." if len(response.content) > 200 else ""))
        print()


def main():
    """Run all conversation examples."""
    print("\n" + "=" * 80)
    print("Example 03: Conversations with Message History")
    print("=" * 80)
    print("\nThis example shows how to maintain conversation history")
    print("for multi-turn interactions with LLMs.")
    print()

    try:
        basic_conversation_example()
    except Exception as e:
        logger.error(f"Basic conversation example failed: {e}")
        print(f"[ERROR] Basic conversation example failed ({type(e).__name__}): {e}\n")

    try:
        interactive_conversation_example()
    except Exception as e:
        logger.error(f"Interactive conversation example failed: {e}")
        print(f"[ERROR] Interactive conversation example failed ({type(e).__name__}): {e}\n")

    try:
        multi_provider_conversation()
    except Exception as e:
        logger.error(f"Multi-provider conversation example failed: {e}")
        print(f"[ERROR] Multi-provider conversation example failed ({type(e).__name__}): {e}\n")

    print("=" * 80)
    print("[SUCCESS] Conversation examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
