# Phase 04: Basic Examples

## Phase Overview

**Purpose**: Implement examples 01-02 (basic invocation and streaming) with both Python scripts and Jupyter notebooks, demonstrating foundational LangChain patterns.

**Outcome**: Working examples showing:
- Basic LLM invocation (`llm.invoke()`)
- Streaming responses (`llm.stream()`)
- All three providers (OpenAI, Anthropic, Gemini)
- Graceful error handling
- Interactive Jupyter notebooks

---

## Why Basic Examples Come Fourth

### Building on Tested Foundation

**Phases 01-03 Created**:
- Project structure
- Configuration utilities (tested)
- Logging utilities (tested)
- Test infrastructure

**Phase 04 Uses Them**:
- Examples use `load_env_config()`, `get_api_key()`
- Examples use `setup_logging()`, `get_logger()`
- Demonstrates utilities in real scenarios
- Shows users how to use the template

### Educational Progression

**Learning Path**:
1. **Example 01**: Simplest possible usage
2. **Example 02**: Add ONE new concept (streaming)
3. Later: Examples 03-04 add more concepts

**Why These Two First**:
- Foundation for all LLM work (invoke and stream)
- No complex concepts (no history, no callbacks)
- Clear, linear code flow
- Easy wins for learners

---

## Task in This Phase

### Task 012: Implement Examples 01-02 with Notebooks
**File**: `task-012-implement-examples-01-02-with-notebooks.md`

**Purpose**: Create first two progressive examples in both Python and Jupyter formats

**Key Activities**:

#### Example 01: Basic Usage
- Create `examples/01_basic.py`:
  - Module docstring explaining purpose
  - Import statements (LangChain providers + langchain_llm utilities)
  - Setup pattern (logging, config loading)
  - Three provider functions:
    - `basic_openai_example()` - ChatOpenAI with gpt-4o-mini
    - `basic_anthropic_example()` - ChatAnthropic with claude-3-5-haiku
    - `basic_gemini_example()` - ChatGoogleGenerativeAI with gemini-2.0-flash
  - `main()` function - Try all providers, graceful error handling
  - `if __name__ == "__main__":` block
  - Extensive comments explaining WHY, not WHAT
  - Temperature=0.7, same prompt for all: "What is machine learning in one sentence?"

#### Example 02: Streaming
- Create `examples/02_streaming.py`:
  - Similar structure to 01_basic.py
  - Three streaming functions (one per provider)
  - Use `llm.stream()` instead of `llm.invoke()`
  - Longer prompt to show streaming effect (3 paragraphs about AI history)
  - Print with `end=""` and `flush=True` for real-time output
  - Comments explaining when to use streaming vs invoke

#### Jupyter Notebooks
- Create `examples/01_basic.ipynb`:
  - Convert 01_basic.py content to cells
  - Markdown cells for explanations
  - Code cells for setup and each provider
  - Can run cells independently
  - Preserve output in saved notebook

- Create `examples/02_streaming.ipynb`:
  - Convert 02_streaming.py content to cells
  - Same cell structure as 01_basic.ipynb
  - Show streaming in notebook context

**Output**:
- `examples/01_basic.py` (~150 lines)
- `examples/02_streaming.py` (~180 lines)
- `examples/01_basic.ipynb` (~12-15 cells)
- `examples/02_streaming.ipynb` (~12-15 cells)

**Total LOC**: ~400-500 lines across 4 files

**Review Scope**: Two complete, working examples demonstrating core patterns

---

## Prerequisites

### Before Starting This Phase

**Phases 01-03 Complete**:
- [ ] Configuration module working
- [ ] Logging module working
- [ ] Tests passing
- [ ] Package installable

**API Keys Required**:
- At least one provider API key in .env file
- Recommended: All three providers for full testing

**LangChain Knowledge**:
- Read LangChain docs on ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI
- Understand invoke() vs stream()
- Know message format basics

**Tools Ready**:
- Python environment with LangChain packages installed
- Jupyter notebook support (for testing notebooks)
- API keys configured

---

## Phase Execution Strategy

### Development Order

1. **Example 01 (Python)**:
   - Write 01_basic.py
   - Test with each provider
   - Verify graceful error handling
   - Add comprehensive comments

2. **Example 01 (Jupyter)**:
   - Convert to notebook format
   - Test cell execution
   - Save with output

3. **Example 02 (Python)**:
   - Write 02_streaming.py
   - Test streaming works
   - Verify output formatting
   - Add comments

4. **Example 02 (Jupyter)**:
   - Convert to notebook format
   - Test streaming in notebook
   - Save with output

### Testing Strategy

**Manual Testing Required**:
```bash
# Test Python scripts
poetry run python examples/01_basic.py
poetry run python examples/02_streaming.py

# Test from different directories
cd examples
poetry run python 01_basic.py
cd ..

# Test Jupyter notebooks
poetry run jupyter notebook examples/
# Run all cells in each notebook
```

**Test Scenarios**:
- [ ] With all three API keys configured
- [ ] With only one API key (others skip gracefully)
- [ ] With no API keys (all skip, no crashes)
- [ ] Run from project root
- [ ] Run from examples/ directory

---

## Success Criteria

### Examples Work Correctly

**Example 01**:
- [ ] All three providers run successfully (with API keys)
- [ ] Skips providers gracefully if no API key
- [ ] Output clearly shows which provider generated which response
- [ ] Same prompt produces comparable responses
- [ ] No errors or exceptions

**Example 02**:
- [ ] Streaming displays tokens in real-time
- [ ] All three providers stream correctly
- [ ] Output is properly formatted (no extra newlines)
- [ ] Shows clear difference from batch (invoke)

### Code Quality

- [ ] All functions have docstrings
- [ ] Extensive inline comments
- [ ] No hardcoded secrets
- [ ] Follows project patterns (setup_logging, load_env_config)
- [ ] `ruff check examples/` passes

### Notebooks Work

- [ ] All cells execute without errors
- [ ] Output preserved in saved notebooks
- [ ] Markdown cells explain concepts
- [ ] Can run cells independently

### Validation Commands

```bash
# Python scripts
poetry run python examples/01_basic.py
poetry run python examples/02_streaming.py

# Code quality
ruff check examples/

# Notebooks (manual)
poetry run jupyter notebook examples/
# Execute all cells, verify output
```

---

## Outputs of This Phase

### Files Created

```
examples/
├── 01_basic.py              # NEW: Basic invocation example (~150 lines)
├── 01_basic.ipynb           # NEW: Jupyter version (~15 cells)
├── 02_streaming.py          # NEW: Streaming example (~180 lines)
└── 02_streaming.ipynb       # NEW: Jupyter version (~15 cells)
```

### Demonstrated Patterns

**Configuration Pattern** (every example uses):
```python
from langchain_llm import setup_logging, get_logger, load_env_config, get_api_key

setup_logging()
logger = get_logger(__name__)
load_env_config()
```

**Provider Pattern** (repeatable):
```python
def basic_provider_example():
    """Example using Provider."""
    api_key = get_api_key("provider")
    llm = ChatProvider(model="model-name", api_key=api_key)
    response = llm.invoke("prompt")
    print(response.content)
```

**Error Handling Pattern**:
```python
try:
    provider_example()
except Exception as e:
    logger.error(f"Provider failed: {e}")
    print(f"[WARNING] Provider skipped: {e}")
```

---

## Common Issues & Solutions

**Issue**: Import errors for LangChain providers
**Solution**: Verify langchain-openai, langchain-anthropic, langchain-google-genai installed

**Issue**: API key not found
**Solution**: Check .env file exists, has correct variable names, load_env_config() called

**Issue**: Streaming not showing in real-time
**Solution**: Ensure `flush=True` in print statements

**Issue**: Jupyter kernel issues
**Solution**: Install ipykernel: `poetry add --group dev ipykernel`

**Issue**: Examples work from root but not from examples/
**Solution**: `load_env_config()` searches upward, should work from any directory

---

## Transition to Next Phase

### Ready for Phase 05 When

**Examples Complete**:
- [ ] 01_basic.py works with all providers
- [ ] 02_streaming.py works with all providers
- [ ] Both have Jupyter notebook versions
- [ ] All tests (manual) pass

**Code Quality**:
- [ ] Ruff check passes
- [ ] Comments are comprehensive
- [ ] No hardcoded secrets

**What's Next** (Phase 05):
- Example 03: Multi-turn conversations (message history)
- Example 04: Advanced features (callbacks, batching)
- Jupyter notebooks for both
- More complex LangChain patterns

**Why This Order**:
- Phase 04 established basic patterns
- Phase 05 builds on them with advanced concepts
- Progressive complexity (basic → streaming → conversation → callbacks)

---

## Related Documents

**Requirements**:
- [001-functional-requirements.md](../requirements/001-functional-requirements.md) - Example requirements

**Designs**:
- [004-examples-design.md](../designs/004-examples-design.md) - Example structure and patterns

**Tasks**:
- [task-012-implement-examples-01-02-with-notebooks.md](../tasks/task-012-implement-examples-01-02-with-notebooks.md)

**Previous/Next**:
- [phase-03-testing-infrastructure.md](phase-03-testing-infrastructure.md) - Previous
- [phase-05-advanced-examples.md](phase-05-advanced-examples.md) - Next

---

## Document Metadata

- **Version**: 1.0
- **Phase Number**: 04 of 06
- **Task Range**: 011 (1 task)
- **Complexity**: Medium
- **Dependencies**: Phases 01-03 complete
- **Status**: Active
- **Owner**: EAD LangChain Template Team
