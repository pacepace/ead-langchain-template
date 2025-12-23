# Design 004: Examples Design

## Document Purpose

This document specifies the design for the progressive examples in the EAD LangChain Template. It defines the learning progression, example structure, and educational principles that guide example implementation.

---

## Overview

### Purpose of Examples

The examples serve three primary purposes:
1. **Education**: Teach LangChain patterns from basic to advanced
2. **Reference**: Show correct usage of langchain_llm utilities
3. **Validation**: Demonstrate that the template works

### Educational Philosophy

- **Progressive Disclosure**: One new concept at a time
- **Hands-On Learning**: Working code over documentation
- **Provider Agnostic**: Same patterns work across OpenAI, Anthropic, Gemini
- **Real-World Patterns**: Production-ready approaches, not toys

---

## Learning Progression

### Overall Arc

```
01_basic        → 02_streaming      → 03_conversation   → 04_advanced
(Simplest)        (One new concept)    (One new concept)    (Production features)

Concepts:
- Invoke          - Stream tokens      - Message history    - Callbacks
- Setup pattern   - Flush output       - System prompts     - Batching
- API keys        - Use cases          - Context            - Cost tracking
- Temperature                          - Multi-turn         - Error handling
```

### Prerequisite Chain

```
No Prerequisites → Example 01 → Example 02 → Example 03 → Example 04
                      ↓             ↓             ↓             ↓
                   Concepts     Add Stream   Add History   Add Callbacks
```

**Key**: Each example builds conceptually but runs independently

---

## Example 01: Basic Usage

### Learning Objectives

1. Understand minimal setup (load config, get API key)
2. See basic LLM invocation (`llm.invoke()`)
3. Recognize provider similarity (same pattern, different imports)
4. Learn temperature parameter

### Structure

```python
# File: examples/01_basic.py

"""
Example 01: Basic LLM Usage

Shows the simplest possible way to use LangChain with different providers.
"""

# Imports
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_llm import get_api_key, get_logger, load_env_config, setup_logging

# Setup (standard pattern for all examples)
setup_logging()
logger = get_logger(__name__)
load_env_config()


# Provider-specific functions (one per provider)
def basic_openai_example():
    """Simple example using OpenAI."""
    logger.info("Running OpenAI example")

    # Get API key
    api_key = get_api_key("openai")

    # Create LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key,
        temperature=0.7,
    )

    # Invoke
    response = llm.invoke("What is machine learning in one sentence?")

    # Output
    print(f"\n{'=' * 80}")
    print("OpenAI (GPT-4o-mini):")
    print(f"{'=' * 80}")
    print(response.content)
    print()


def basic_anthropic_example():
    """Simple example using Anthropic Claude."""
    # Similar structure to OpenAI
    pass


def basic_gemini_example():
    """Simple example using Google Gemini."""
    # Similar structure to OpenAI
    pass


# Main function (tries all providers, skips if API key missing)
def main():
    """Run all basic examples."""
    print("\n" + "=" * 80)
    print("Example 01: Basic LLM Usage")
    print("=" * 80)

    # Try each provider
    try:
        basic_openai_example()
    except Exception as e:
        print(f"[WARNING] OpenAI example skipped: {e}\n")

    try:
        basic_anthropic_example()
    except Exception as e:
        print(f"[WARNING] Anthropic example skipped: {e}\n")

    try:
        basic_gemini_example()
    except Exception as e:
        print(f"[WARNING] Gemini example skipped: {e}\n")

    print("=" * 80)
    print("[SUCCESS] Basic examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
```

### Design Principles

**Simplicity First**:
- Absolute minimum code
- One function per provider
- No abstractions, no helper functions
- Clear, linear flow

**Graceful Degradation**:
- Try/except around each provider
- Print warnings (not errors) for missing keys
- Continue with other providers if one fails
- Success even if all providers skip

**Consistent Pattern**:
- Same structure for all three providers
- Same prompt for comparison
- Same output format

**Educational Comments**:
- Explain WHY each step happens
- Link to concepts (temperature, model names)
- Reference documentation where appropriate

### Example Output

```
================================================================================
Example 01: Basic LLM Usage
================================================================================

================================================================================
OpenAI (GPT-4o-mini):
================================================================================
Machine learning is a subset of artificial intelligence that enables computers
to learn and improve from experience without being explicitly programmed.

================================================================================
Anthropic (Claude 3.5 Haiku):
================================================================================
Machine learning is a type of artificial intelligence where computer systems
learn patterns from data to make predictions or decisions without being
explicitly programmed.

================================================================================
Google Gemini (2.0 Flash):
================================================================================
Machine learning is an application of artificial intelligence that allows
systems to learn and improve from experience without being explicitly programmed.

================================================================================
[SUCCESS] Basic examples complete!
================================================================================
```

---

## Example 02: Streaming Responses

### Learning Objectives

1. Understand streaming vs batch responses
2. Learn when to use streaming (long responses, UX)
3. See `.stream()` method usage
4. Handle chunk processing

### New Concepts

**From Example 01**:
- setup_logging(), load_env_config(), get_api_key()
- Creating LLM instances
- Basic invocation

**New in Example 02**:
- `.stream()` method (instead of `.invoke()`)
- Iterating over chunks
- `flush=True` for real-time output
- Longer prompts (to show streaming effect)

### Structure

```python
def streaming_openai_example():
    """Streaming example using OpenAI."""
    logger.info("Running OpenAI streaming example")

    api_key = get_api_key("openai")
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.7)

    # DIFFERENT: Use longer prompt to show streaming
    prompt = "Explain the history of artificial intelligence in 3 paragraphs."

    print(f"\n{'=' * 80}")
    print("OpenAI (GPT-4o-mini) - Streaming:")
    print(f"{'=' * 80}")

    # DIFFERENT: Use .stream() instead of .invoke()
    for chunk in llm.stream(prompt):
        # DIFFERENT: Print immediately with flush
        print(chunk.content, end="", flush=True)

    print("\n")  # Newline after stream completes
```

### Design Principles

**Show the Difference**:
- Side-by-side comparison possible (invoke vs stream)
- Longer prompt makes streaming visible
- Comments highlight new patterns

**Real-Time Feeling**:
- `flush=True` ensures immediate output
- `end=""` prevents newlines between chunks
- Final `print()` adds closing newline

**Use Cases**:
```python
"""
When to use streaming:
- Long responses (multi-paragraph)
- User-facing applications (better UX)
- Real-time feedback (chatbots)

When to use invoke:
- Short responses
- Batch processing
- When you need full response at once
"""
```

---

## Example 03: Conversations

### Learning Objectives

1. Understand message history concept
2. Learn message types (System, Human, AI)
3. See how context affects responses
4. Build multi-turn conversations

### New Concepts

**From Previous Examples**:
- Setup pattern
- LLM creation
- Basic invocation or streaming

**New in Example 03**:
- `SystemMessage`, `HumanMessage`, `AIMessage`
- Message history list
- Passing history to `.invoke()`
- Appending responses to history

### Structure

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


def conversation_openai_example():
    """Multi-turn conversation example with OpenAI."""
    logger.info("Running OpenAI conversation example")

    api_key = get_api_key("openai")
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.7)

    print(f"\n{'=' * 80}")
    print("OpenAI (GPT-4o-mini) - Conversation:")
    print(f"{'=' * 80}")

    # NEW: Initialize conversation history
    history = [
        SystemMessage(content="You are a helpful AI assistant specializing in Python programming."),
    ]

    # Turn 1: First question
    history.append(HumanMessage(content="What is Python?"))
    print(f"\nUser: {history[-1].content}")

    # NEW: Pass history (not just string)
    response = llm.invoke(history)
    print(f"Assistant: {response.content}")

    # NEW: Append AI response to history
    history.append(AIMessage(content=response.content))

    # Turn 2: Follow-up question (uses context)
    history.append(HumanMessage(content="What are its main uses?"))
    print(f"\nUser: {history[-1].content}")

    response = llm.invoke(history)
    print(f"Assistant: {response.content}")
    history.append(AIMessage(content=response.content))

    # Turn 3: Another follow-up (deeper context)
    history.append(HumanMessage(content="How does it compare to JavaScript?"))
    print(f"\nUser: {history[-1].content}")

    response = llm.invoke(history)
    print(f"Assistant: {response.content}")

    print()
```

### Design Principles

**Progressive Conversation**:
- Each turn builds on previous
- Show how context affects responses
- Demonstrate system message usage

**Explicit History Management**:
- Clear list structure
- Explicit appending
- Visible message types

**Educational Flow**:
```python
# Comments explain each step
# 1. Create history with system prompt
# 2. Add user message
# 3. Get response
# 4. Add response to history
# 5. Repeat
```

---

## Example 04: Advanced Features

### Learning Objectives

1. Understand LangChain callbacks
2. Learn batch processing
3. Track token usage and costs
4. Handle errors in production scenarios

### New Concepts

**From Previous Examples**:
- All basic patterns
- Message history (optional to use)

**New in Example 04**:
- Custom `BaseCallbackHandler`
- `.batch()` method
- Token counting
- Error handling patterns
- Performance comparison

### Structure

```python
from langchain_core.callbacks import BaseCallbackHandler


# NEW: Custom callback for tracking
class TokenCounterCallback(BaseCallbackHandler):
    """
    Callback to count tokens and track usage.

    Demonstrates:
    - Implementing BaseCallbackHandler
    - Hooking into LLM lifecycle
    - Tracking metrics
    """

    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def on_llm_end(self, response, **kwargs):
        """Called when LLM completes."""
        # Extract token usage from response
        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            self.prompt_tokens += usage.get("prompt_tokens", 0)
            self.completion_tokens += usage.get("completion_tokens", 0)
            self.total_tokens += usage.get("total_tokens", 0)

    def report(self):
        """Print usage summary."""
        print(f"\nToken Usage:")
        print(f"  Prompt tokens: {self.prompt_tokens}")
        print(f"  Completion tokens: {self.completion_tokens}")
        print(f"  Total tokens: {self.total_tokens}")


def advanced_callbacks_example():
    """Demonstrate callbacks for token tracking."""
    # Create callback
    callback = TokenCounterCallback()

    # Create LLM with callback
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=get_api_key("openai"),
        callbacks=[callback],  # NEW: Pass callbacks
    )

    # Make some calls
    llm.invoke("What is Python?")
    llm.invoke("Explain machine learning.")

    # Report usage
    callback.report()


def advanced_batching_example():
    """Demonstrate batch processing for efficiency."""
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=get_api_key("openai"))

    # Multiple prompts
    prompts = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?",
    ]

    print("\n" + "=" * 80)
    print("Batch Processing:")
    print("=" * 80)

    # NEW: Use .batch() for parallel processing
    import time
    start = time.time()
    responses = llm.batch(prompts)
    batch_time = time.time() - start

    for i, response in enumerate(responses):
        print(f"\nPrompt {i + 1}: {prompts[i]}")
        print(f"Response: {response.content[:100]}...")

    print(f"\nBatch processing time: {batch_time:.2f}s")

    # Compare to sequential
    start = time.time()
    for prompt in prompts:
        llm.invoke(prompt)
    sequential_time = time.time() - start

    print(f"Sequential processing time: {sequential_time:.2f}s")
    print(f"Speedup: {sequential_time / batch_time:.2f}x")
```

### Design Principles

**Production Patterns**:
- Real-world callback usage
- Error handling
- Performance measurement
- Cost tracking

**Show Trade-Offs**:
- Batch vs sequential performance
- Callback overhead
- When to use each pattern

**Extensible Examples**:
```python
# Show how users can extend
class CustomCallback(BaseCallbackHandler):
    """Users can create their own callbacks."""

    def on_llm_start(self, serialized, prompts, **kwargs):
        # Log start time
        pass

    def on_llm_end(self, response, **kwargs):
        # Log end time, calculate duration
        pass

    def on_llm_error(self, error, **kwargs):
        # Handle errors
        pass
```

---

## Dual Format (Python + Jupyter)

### Jupyter Notebook Structure

**Same Content, Different Format**:
```
Cell 1 (Markdown):
  # Example 01: Basic LLM Usage
  This example demonstrates...

Cell 2 (Code):
  # Setup
  from langchain_llm import setup_logging, load_env_config
  setup_logging()
  load_env_config()

Cell 3 (Markdown):
  ## OpenAI Example
  First, let's try OpenAI...

Cell 4 (Code):
  def basic_openai_example():
      ...
  basic_openai_example()

Cell 5 (Markdown):
  ## Anthropic Example
  Now let's try Anthropic...

Cell 6 (Code):
  def basic_anthropic_example():
      ...
  basic_anthropic_example()
```

### Conversion Process

**Python → Jupyter**:
1. Docstrings become markdown cells
2. Code blocks become code cells
3. Comments become markdown annotations
4. Function calls become separate cells

**Benefits**:
- Interactive exploration
- Cell-by-cell execution
- Output preserved in notebook
- Better for learning/experimentation

---

## Common Patterns Across All Examples

### Setup Pattern (Every Example)

```python
from langchain_llm import setup_logging, get_logger, load_env_config

setup_logging()
logger = get_logger(__name__)
load_env_config()
```

**Why Consistent**:
- Users learn pattern once
- Can copy-paste to their code
- Reduces cognitive load

### Provider Function Pattern

```python
def <concept>_<provider>_example():
    """<One-line description>."""
    logger.info(f"Running {provider} {concept} example")

    # Get API key
    api_key = get_api_key(provider)

    # Create LLM
    llm = ChatProvider(model=model_name, api_key=api_key, ...)

    # Do the thing
    response = llm.invoke(...)

    # Show output
    print(...)
```

### Error Handling Pattern

```python
try:
    provider_example()
except Exception as e:
    logger.error(f"{Provider} example failed: {e}")
    print(f"[WARNING] {Provider} example skipped: {e}\n")
```

**Graceful**:
- Logs error for debugging
- Prints user-friendly warning
- Continues with other providers

---

## Testing Strategy for Examples

### Manual Testing (Primary)

**Process**:
1. Run each example: `python examples/01_basic.py`
2. Verify output looks correct
3. Test with different API keys
4. Test with missing API keys (should skip gracefully)

**Checklist**:
- [ ] Example runs without errors
- [ ] Output is correct
- [ ] Skips gracefully if API key missing
- [ ] Works from different directories

### Automated Testing (Comprehensive)

**IMPLEMENTED**: All examples have comprehensive test coverage (>80%) in `tests/unit/test_examples.py`

**Testing Approach**:
- Mock LLM responses using unittest.mock to avoid API calls
- Test that examples call correct methods with correct parameters
- Verify configuration usage (get_api_key, get_model_name)
- Test error handling in main() functions
- Validate conversation history management
- Test callback functionality (TokenCounterCallback)

**Coverage Targets**:
- 01_basic.py: >80% (currently ~94%)
- 02_streaming.py: >80% (currently ~87%)
- 03_conversation.py: >80% (currently ~84%)
- 04_advanced.py: >80% (currently ~92%)

**Example Test Pattern**:
```python
# tests/unit/test_examples.py

def test_basic_openai_example_with_mock(mock_env_vars, monkeypatch, capsys):
    """Test basic_openai_example with mocked LLM."""
    # Create mock LLM
    mock_llm = Mock()
    mock_llm.invoke.return_value = Mock(content="Test response")

    # Mock ChatOpenAI class
    monkeypatch.setattr(basic_01, "ChatOpenAI", Mock(return_value=mock_llm))

    # Run function
    basic_01.basic_openai_example()

    # Verify correct calls were made
    assert mock_llm.invoke.called

    # Verify output
    captured = capsys.readouterr()
    assert "OpenAI" in captured.out
```

**Running Tests**:
```bash
pytest tests/unit/test_examples.py -v                      # All example tests
pytest tests/unit/test_examples.py --cov=examples          # With coverage
```

**Why Test Examples?**
- Demonstrates testing patterns for LLM applications
- Prevents regressions when updating LangChain versions
- Shows how to test code dependent on external APIs
- Validates configuration and error handling without API calls

---

## Documentation Requirements

### Docstrings

**Module Level**:
```python
"""
Example 0X: Title

Brief description of what this example demonstrates.

Shows:
- Concept 1
- Concept 2
- Concept 3

Prerequisites:
- Example 0Y (if applicable)
- Concepts from previous examples
"""
```

**Function Level**:
```python
def example_function():
    """
    One-line description.

    Demonstrates:
    - Thing 1
    - Thing 2
    """
```

### Inline Comments

**What to Comment**:
- Why this approach (not what the code does)
- When to use this pattern
- Gotchas and edge cases
- Links to documentation

**What NOT to Comment**:
- Obvious code (`x = 5  # Set x to 5`)
- Repeating function names
- Implementation details

---

## Maintenance Guidelines

### Adding New Examples

**Process**:
1. Determine concept to teach
2. Identify prerequisite examples
3. Write Python script (`.py`)
4. Convert to Jupyter notebook (`.ipynb`)
5. Update README with new example
6. Test manually

**Numbering**: Use next available number (05, 06, ...)

### Updating Existing Examples

**When to Update**:
- LangChain API changes
- Provider SDK changes
- Better patterns discovered
- User feedback

**Process**:
1. Update `.py` file
2. Update corresponding `.ipynb`
3. Test both versions
4. Update README if needed

---

## Related Documents

- **Previous**: [003-logging-design.md](003-logging-design.md) - Logging design
- **Next**: [005-testing-strategy.md](005-testing-strategy.md) - Testing strategy
- **See Also**:
  - [requirements/001-functional-requirements.md](../requirements/001-functional-requirements.md) - Example requirements
  - [000-architecture-overview.md](000-architecture-overview.md) - Progressive disclosure principle

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
