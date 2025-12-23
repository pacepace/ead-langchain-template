# Task 009: Implement Basic Examples (01-02) with Notebooks

## Task Context

**Phase**: 04 - Basic Examples
**Sequence**: Ninth task (Phase 04 complete)
**Complexity**: Medium
**Output**: ~400 LOC (4 files: 2 Python scripts + 2 notebooks)

### Why This Task Exists

Educational examples demonstrate:
- How to use the utilities built in Phases 01-03
- Basic LangChain patterns (invoke, stream)
- Provider-agnostic code
- Progressive learning (01→02)

This task creates the foundation examples that later examples build on.

---

## Prerequisites

### Completed Tasks

- [x] **Tasks 001-010**: All core utilities implemented and tested

### Required Knowledge

**LangChain**:
- ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI classes
- `.invoke()` method
- `.stream()` method
- Model parameters (temperature)

**Jupyter**:
- Notebook structure (cells)
- Markdown cells vs code cells
- Converting Python scripts to notebooks

---

## Research Required

### LangChain Provider Documentation

**Read**:
- ChatOpenAI docs: https://python.langchain.com/docs/integrations/chat/openai
- ChatAnthropic docs: https://python.langchain.com/docs/integrations/chat/anthropic
- ChatGoogleGenerativeAI docs: https://python.langchain.com/docs/integrations/chat/google_generative_ai

**Key Concepts**:
- Model names for each provider
- invoke() vs stream() differences
- Temperature parameter
- Streaming chunk handling

---

## Code to Explore

**Design**: `docs/complete/designs/004-examples-design.md` - Example patterns
**Utilities**: `src/langchain_llm/` - Functions you'll use

---

## Task Description

### Objective

Create Examples 01 and 02 in both Python and Jupyter formats, demonstrating basic LLM usage and streaming with all three providers.

### Requirements

#### Example 01: Basic Usage (01_basic.py + .ipynb)

**Python Script** (~150 lines):

**Structure**:
- Module docstring explaining purpose
- Imports (LangChain providers + langchain_llm utilities)
- Setup (setup_logging, load_env_config)
- Three functions:
  - `basic_openai_example()` - ChatOpenAI with gpt-5-nano
  - `basic_anthropic_example()` - ChatAnthropic with claude-3-haiku-20240307
  - `basic_gemini_example()` - ChatGoogleGenerativeAI with gemini-2.0-flash-lite
- `main()` - Try all providers, catch errors gracefully
- `if __name__ == "__main__"` block

**Each Provider Function**:
- Get API key: `api_key = get_api_key("provider")`
- Create LLM with model and temperature
- Invoke with same prompt: "What is machine learning in one sentence?"
- Print formatted output

**Error Handling in main()**:
```python
try:
    basic_openai_example()
except Exception as e:
    logger.error(f"OpenAI example failed: {e}")
    print(f"[WARNING] OpenAI example skipped: {e}\n")
```

**Comments**: Explain WHY, not WHAT. Explain temperature, model choices, when to use invoke.

**Jupyter Notebook** (~15 cells):
- Convert Python script to cells
- Markdown cells for section headers
- Code cells for each provider
- Preserve output when saving

#### Example 02: Streaming (02_streaming.py + .ipynb)

**Python Script** (~180 lines):

**Structure**: Similar to 01_basic.py but with streaming

**Each Provider Function**:
- Get API key
- Create LLM
- Longer prompt (3 paragraphs) to show streaming: "Explain the history of artificial intelligence in 3 paragraphs"
- Stream with: `for chunk in llm.stream(prompt):`
- Print chunks: `print(chunk.content, end="", flush=True)`
- Final newline after stream

**Comments**: Explain when to use streaming vs invoke, why flush=True, use cases.

**Jupyter Notebook** (~15 cells):
- Convert to notebook format
- Markdown explains streaming concept
- Code cells show streaming in action

### Constraints

- All functions have docstrings
- Extensive inline comments
- No hardcoded API keys
- Graceful error handling
- Same prompt across providers (for comparison)
- No phase/task references in comments

---

## Testing Examples

**IMPORTANT**: Examples have comprehensive test coverage (>80%) using mocked LLM responses.

### Test File Location

`tests/unit/test_examples.py` - Comprehensive tests for all example modules

### Testing Approach

Examples are tested using **Test-Driven Development** principles adapted for demonstration code:

1. **Import Tests**: Verify modules can be imported and have required functions
2. **Mock LLM Responses**: Use unittest.mock to avoid actual API calls
3. **Behavior Tests**: Verify examples call correct methods with correct parameters
4. **Error Handling Tests**: Verify examples handle failures gracefully
5. **Integration Tests**: Verify examples use langchain_llm utilities correctly

### Example Test Pattern

```python
def test_basic_openai_example_with_mock(mock_env_vars, monkeypatch, capsys):
    """Test basic_openai_example with mocked LLM."""
    # Create mock LLM
    mock_llm = Mock()
    mock_llm.invoke.return_value = Mock(content="Test response")

    # Mock ChatOpenAI class
    monkeypatch.setattr(basic_01, "ChatOpenAI", Mock(return_value=mock_llm))

    # Run function
    basic_01.basic_openai_example()

    # Verify correct calls made
    assert mock_llm.invoke.called
```

### Running Tests

```bash
# Run example tests
pytest tests/unit/test_examples.py -v

# Check coverage (target: >80%)
pytest tests/unit/test_examples.py --cov=examples --cov-report=term
```

### Why Test Examples?

- **Demonstrate testing patterns** for LLM applications
- **Prevent regressions** when updating LangChain versions
- **Verify configuration** works correctly without API calls
- **Show best practices** for testing code that uses external APIs

---

## Success Criteria

### Functional

- [ ] 01_basic.py works with all providers
- [ ] 02_streaming.py works with all providers
- [ ] Both have Jupyter notebooks
- [ ] Examples skip providers gracefully if no API key
- [ ] Can run from any directory

### Quality

- [ ] Functions have docstrings
- [ ] Comprehensive comments
- [ ] No hardcoded secrets
- [ ] `ruff check examples/` passes

### Testing

- [ ] Example tests exist in `tests/unit/test_examples.py`
- [ ] Tests cover all provider examples (OpenAI, Anthropic, Gemini)
- [ ] Tests use mocks to avoid actual API calls
- [ ] Test coverage >80% for example modules
- [ ] All tests pass: `pytest tests/unit/test_examples.py`

### Integration

- [ ] Examples use langchain_llm utilities correctly
- [ ] Logging shows enhanced format
- [ ] Configuration loaded from .env
- [ ] Examples use `get_model_name()` with fallback pattern

---

## Expected Approach (Ideal Path)

### Step 1: Read Design Doc

Thoroughly read `docs/complete/designs/004-examples-design.md` for patterns.

### Step 2: Create 01_basic.py

Start with module docstring, imports, setup, then implement provider functions one at a time.

### Step 3: Test 01_basic.py

```bash
# Ensure .env exists with at least one API key
cp .env.example .env
# Edit .env with real key

poetry run python examples/01_basic.py
```

### Step 4: Create 01_basic.ipynb

Convert script to notebook format. Test cells run successfully.

### Step 5: Create 02_streaming.py

Similar to 01_basic but with streaming pattern.

### Step 6: Test 02_streaming.py

```bash
poetry run python examples/02_streaming.py
# Should see tokens appearing in real-time
```

### Step 7: Create 02_streaming.ipynb

Convert to notebook, test execution.

### Step 8: Validate All Examples

```bash
# Both scripts
poetry run python examples/01_basic.py
poetry run python examples/02_streaming.py

# Jupyter
poetry run jupyter notebook examples/
# Run all cells in both notebooks
```

---

## Testing Strategy

**Test Scenarios**:
- [ ] With all three API keys configured
- [ ] With only OpenAI key (others skip)
- [ ] With no keys (all skip, no crash)
- [ ] Run from project root
- [ ] Run from examples/ directory

---

## Troubleshooting

**Issue**: Import errors for LangChain
**Solution**: Check langchain-openai, langchain-anthropic, langchain-google-genai installed

**Issue**: API key not found
**Solution**: Check .env exists, has correct variable names, load_env_config() called

**Issue**: Streaming not real-time
**Solution**: Ensure `flush=True` in print statements

**Issue**: Jupyter kernel issues
**Solution**: `poetry run python -m ipykernel install --user --name=ead-langchain`

---

## Next Steps

After this task:

1. **Phase 04 Complete**: Basic examples working

2. **Move to Task 010**:
   - Implement examples 03-04 (conversations, advanced)

---

## Related Documents

**Design**: [004-examples-design.md](../designs/004-examples-design.md)
**Requirements**: [001-functional-requirements.md](../requirements/001-functional-requirements.md)
**Phase**: [phase-04-basic-examples.md](../phases/phase-04-basic-examples.md)
**Previous**: [task-008-create-enforcement-tests.md](task-008-create-enforcement-tests.md)
**Next**: [task-010-implement-advanced-examples.md](task-010-implement-advanced-examples.md)

---

## Document Metadata

- **Task ID**: 009
- **Phase**: 04 - Basic Examples
- **LOC Output**: ~400 lines (4 files)
- **Complexity**: Medium
- **Prerequisites**: Tasks 001-008 complete
