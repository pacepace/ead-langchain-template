# Task 010: Implement Advanced Examples (03-04) with Notebooks

## Task Context

**Phase**: 05 - Advanced Examples
**Sequence**: Tenth task (Phase 05 complete)
**Complexity**: Medium-High
**Output**: ~600 LOC (4 files: 2 Python scripts + 2 notebooks)

### Why This Task Exists

Advanced examples demonstrate:
- Multi-turn conversations (message history)
- Production patterns (callbacks, batching)
- Cost tracking and metrics
- Real-world use cases

Completes the progressive learning arc (basic → streaming → conversation → production).

---

## Prerequisites

### Completed Tasks

- [x] **Task 009**: Examples 01-02 created

### Required Knowledge

**LangChain Advanced**:
- Message types (SystemMessage, HumanMessage, AIMessage)
- Message history management
- BaseCallbackHandler
- Batch processing

**Python**:
- Class inheritance
- Method overriding
- Performance measurement (time module)

---

## Research Required

### LangChain Callbacks

**Read**:
- BaseCallbackHandler docs: https://python.langchain.com/docs/modules/callbacks/
- Callback methods (on_llm_start, on_llm_end, on_llm_error)
- Token usage tracking

**Key Concepts**:
- When callbacks are called
- Accessing response metadata
- Multiple callbacks

### LangChain Batch Processing

**Read**:
- Batch method documentation
- Async vs sync batching

**Key Concepts**:
- When to use batch()
- Performance benefits
- Error handling in batches

---

## Code to Explore

**Design**: `docs/complete/designs/004-examples-design.md` - Advanced patterns
**Examples**: `examples/01_basic.py` - Pattern to follow

---

## Task Description

### Objective

Create Examples 03 and 04 in both Python and Jupyter formats, demonstrating message history and production-ready patterns.

### Requirements

#### Example 03: Conversations (03_conversation.py + .ipynb)

**Python Script** (~250 lines):

**Structure**:
- Module docstring
- Import message types from langchain_core.messages
- Setup pattern (logging, config)
- Three conversation functions (one per provider)

**Each Conversation Function**:
```python
def conversation_provider_example():
    """Multi-turn conversation with Provider."""
    # Get API key, create LLM

    # Initialize history with SystemMessage
    history = [
        SystemMessage(content="You are a Python programming tutor."),
    ]

    # Turn 1
    history.append(HumanMessage(content="What is Python?"))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))

    # Turn 2 (uses context from turn 1)
    history.append(HumanMessage(content="What are its main uses?"))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))

    # Turn 3 (uses context from turns 1-2)
    history.append(HumanMessage(content="How does it compare to JavaScript?"))
    response = llm.invoke(history)
```

**Comments**: Explain message types, system prompt usage, context retention.

**Jupyter Notebook** (~18 cells):
- Markdown explaining message history
- Show conversation building step-by-step
- Interactive exploration

#### Example 04: Advanced (04_advanced.py + .ipynb)

**Python Script** (~300 lines):

**Custom Callback Class** (~50 lines):
```python
class TokenCounterCallback(BaseCallbackHandler):
    """
    Callback to count tokens and track usage.

    Demonstrates LangChain callback system for metrics collection.
    """

    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def on_llm_end(self, response, **kwargs):
        """Extract token usage from response."""
        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            self.total_tokens += usage.get("total_tokens", 0)
            # ...

    def report(self):
        """Print usage summary."""
        print(f"\nToken Usage:")
        print(f"  Total: {self.total_tokens}")
```

**Callback Example Function** (~60 lines):
- Create callback instance
- Create LLM with callback
- Make multiple calls
- Report metrics

**Batch Processing Function** (~80 lines):
- Multiple prompts list (strings)
- Batch processing: `responses = llm.batch(prompts)`
  - Note: LangChain's `batch()` makes separate API calls (one per prompt)
  - Benefit is convenience and potential parallelization, not API call reduction
  - Pass strings directly (not HumanMessage objects)
- Performance measurement
- Show total processing time

**Comments**: Explain what LangChain's batch() does (convenience wrapper), when to use it, production considerations.

**Internal Logging Requirement:**
```python
from langchain_llm import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

# Use throughout
logger.info("Starting example")
logger.error(f"Error: {e}")
```

Demonstrates production logging pattern alongside educational `print()` statements.

**Jupyter Notebook** (~23 cells):
- Separate sections for callbacks and batching
- Markdown explains concepts
- Show metrics in output cells

### Constraints

- All functions have docstrings
- Extensive comments explaining WHY
- No hardcoded secrets
- Demonstrate production patterns
- No phase/task references

---

## Testing Examples

**IMPORTANT**: Advanced examples have comprehensive test coverage (>80%) using mocked LLM responses.

### Test File Location

`tests/unit/test_examples.py` - Contains tests for all examples including advanced features

### Testing Approach

Advanced examples follow **Test-Driven Development** principles:

1. **Write Tests First**: Define expected behavior before implementation
2. **Mock LLM Calls**: Use unittest.mock to simulate provider responses
3. **Test Callbacks**: Verify TokenCounterCallback tracks usage correctly
4. **Test Batch Processing**: Verify batch() method is called with multiple prompts
5. **Test Conversation History**: Verify message accumulation across turns

### Example Test Patterns

**Testing Callbacks:**
```python
def test_token_counter_callback_tracks_usage():
    """Test that TokenCounterCallback tracks token usage."""
    callback = TokenCounterCallback()

    # Simulate LLM response with token metadata
    mock_response = Mock()
    mock_response.llm_output = {
        "token_usage": {"total_tokens": 30},
    }

    callback.on_llm_end(mock_response)
    summary = callback.get_summary()
    assert summary["total_tokens"] == 30
```

**Testing Batch Processing:**
```python
def test_batch_processing_uses_batch_method(mock_env_vars, monkeypatch):
    """Test that batch processing calls batch() method."""
    mock_llm = Mock()
    mock_llm.batch.return_value = [
        Mock(content="Response 1"),
        Mock(content="Response 2"),
    ]

    monkeypatch.setattr(advanced_04, "ChatOpenAI", Mock(return_value=mock_llm))
    advanced_04.batch_processing_example()

    mock_llm.batch.assert_called_once()
```

### Running Tests

```bash
# Run all example tests
pytest tests/unit/test_examples.py -v

# Check coverage for advanced examples
pytest tests/unit/test_examples.py --cov=examples/03_conversation.py --cov=examples/04_advanced.py

# Target: >80% coverage
```

### Why Test Advanced Examples?

- **Validate callbacks work** without making actual API calls
- **Test conversation logic** independently of LLM responses
- **Verify batch processing** uses correct LangChain methods
- **Prevent regressions** when updating dependencies
- **Demonstrate advanced testing patterns** for production LLM applications

---

## Success Criteria

### Functional

- [ ] 03_conversation.py works, shows context retention
- [ ] 04_advanced.py works, callbacks collect metrics
- [ ] Batching shows performance improvement
- [ ] All have Jupyter notebooks
- [ ] Run from any directory

### Quality

- [ ] Docstrings on all functions
- [ ] Comments explain concepts
- [ ] `ruff check examples/` passes

### Testing

- [ ] Tests exist in `tests/unit/test_examples.py` for advanced examples
- [ ] TokenCounterCallback has unit tests
- [ ] Conversation examples tested with mocked providers
- [ ] Batch processing tested with mock responses
- [ ] Test coverage >80% for 03_conversation.py and 04_advanced.py
- [ ] All example tests pass: `pytest tests/unit/test_examples.py`

---

## Expected Approach (Ideal Path)

### Step 1: Research LangChain

Read message types and callback documentation thoroughly.

### Step 2: Implement 03_conversation.py

Start with one provider, then replicate for others.

### Step 3: Test Conversations

```bash
poetry run python examples/03_conversation.py
# Verify context retained across turns
```

### Step 4: Create 03_conversation.ipynb

Convert to notebook, test cells.

### Step 5: Implement 04_advanced.py

Start with callback class, test it works, then add batching.

### Step 6: Test Advanced Features

```bash
poetry run python examples/04_advanced.py
# Verify callbacks report metrics
# Verify batching is faster
```

### Step 7: Create 04_advanced.ipynb

Convert to notebook, test execution.

### Step 8: Validate All Examples

Test all 4 examples (01-04) work together.

---

## Testing Strategy

**Manual Testing**:
```bash
poetry run python examples/03_conversation.py
poetry run python examples/04_advanced.py

# Verify:
# - Conversations show context
# - Callbacks report tokens
# - Batch faster than sequential
```

---

## Troubleshooting

**Issue**: Message history doesn't retain context
**Solution**: Verify AIMessage with response.content appended to history

**Issue**: Callbacks not called
**Solution**: Pass callbacks to LLM constructor: `ChatOpenAI(callbacks=[cb])`

**Issue**: Batch() passes wrong input type (ValueError)
**Solution**: Pass strings directly: `llm.batch(prompts)`, not `llm.batch([HumanMessage(content=p) for p in prompts])`

**Issue**: Token usage not available
**Solution**: Some providers don't return usage, explain in comments

---

## Next Steps

After this task, **Phase 05 complete!**

1. **Validate**:
   All 4 examples (01-04) working

2. **Move to Task 013**:
   - Write comprehensive README

---

## Related Documents

**Design**: [004-examples-design.md](../designs/004-examples-design.md)
**Phase**: [phase-05-advanced-examples.md](../phases/phase-05-advanced-examples.md)
**Previous**: [task-009-implement-basic-examples.md](task-009-implement-basic-examples.md)
**Next**: [task-011-write-comprehensive-readme.md](task-011-write-comprehensive-readme.md)

---

## Document Metadata

- **Task ID**: 010
- **Phase**: 05
- **LOC Output**: ~600 lines (4 files)
- **Complexity**: Medium-High
