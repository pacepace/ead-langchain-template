# Phase 05: Advanced Examples

## Phase Overview

**Purpose**: Implement examples 03-04 (conversations and advanced features) with both Python scripts and Jupyter notebooks, demonstrating production-ready LangChain patterns.

**Outcome**: Complete example suite with:
- Multi-turn conversations with message history (Example 03)
- Advanced features: callbacks, batching, cost tracking (Example 04)
- All four examples in Python and Jupyter formats
- Progressive learning path complete

---

## Why Advanced Examples Come Fifth

### Completing the Learning Arc

**Examples 01-02 (Phase 04)**:
- Basic invoke
- Streaming responses

**Examples 03-04 (Phase 05)**:
- Message history (conversations)
- Production patterns (callbacks, batching)

**Progressive Complexity**:
```
01 (simplest) → 02 (streaming) → 03 (context) → 04 (production)
```

### Building on Fundamentals

**Users Now Know**:
- How to set up configuration
- Basic LLM invocation
- Streaming pattern
- Error handling

**Can Learn Advanced**:
- Managing conversation state
- Tracking usage/costs
- Batch processing for efficiency
- Custom callbacks

---

## Task in This Phase

### Task 013: Implement Examples 03-04 with Notebooks
**File**: `task-013-implement-examples-03-04-with-notebooks.md`

**Purpose**: Create advanced examples demonstrating production-ready patterns

**Key Activities**:

#### Example 03: Conversations
- Create `examples/03_conversation.py`:
  - Module docstring explaining message history
  - Import message types (SystemMessage, HumanMessage, AIMessage)
  - Three conversation functions (one per provider):
    - Initialize history with SystemMessage
    - Add HumanMessage, get response
    - Append AIMessage to history
    - Continue for 3 turns, showing context retention
  - Demonstrate how context affects responses
  - Show system message usage (personality/instructions)
  - Comments explaining when/why to use conversations

#### Example 04: Advanced Features
- Create `examples/04_advanced.py`:
  - Module docstring explaining production features
  - Custom callback implementation:
    - Class extending BaseCallbackHandler
    - Track tokens, timing, costs
    - on_llm_start, on_llm_end, on_llm_error hooks
  - Batch processing demonstration:
    - Multiple prompts processed in parallel
    - Performance comparison (batch vs sequential)
    - When to use batching
  - Error handling patterns for production
  - Resource cleanup examples

#### Jupyter Notebooks
- Create `examples/03_conversation.ipynb`:
  - Convert 03_conversation.py to cells
  - Markdown cells explain message types
  - Show conversation building step-by-step
  - Interactive exploration of history

- Create `examples/04_advanced.ipynb`:
  - Convert 04_advanced.py to cells
  - Separate callbacks and batching into sections
  - Show metrics/results in output cells
  - Performance graphs (optional)

**Output**:
- `examples/03_conversation.py` (~250 lines)
- `examples/04_advanced.py` (~300 lines)
- `examples/03_conversation.ipynb` (~15-20 cells)
- `examples/04_advanced.ipynb` (~20-25 cells)

**Total LOC**: ~600-700 lines across 4 files

**Review Scope**: Two advanced examples with production patterns

---

## Prerequisites

### Before Starting This Phase

**Phase 04 Complete**:
- [ ] Examples 01-02 working
- [ ] Basic patterns established
- [ ] Jupyter notebook workflow validated

**LangChain Knowledge Required**:
- Message types (System, Human, AI)
- Conversation history management
- BaseCallbackHandler interface
- Batch processing methods

**Research Before Starting**:
- Read LangChain callbacks documentation
- Review LangChain batch() method docs
- Understand message history concepts
- Study callback hook timing

---

## Phase Execution Strategy

### Development Order

1. **Example 03 (Python)**:
   - Implement conversation functions
   - Test 3-turn conversations
   - Verify context retention
   - Add comprehensive comments

2. **Example 03 (Jupyter)**:
   - Convert to notebook
   - Add markdown explanations
   - Test interactive execution

3. **Example 04 (Python)**:
   - Implement callback class
   - Implement batching example
   - Test metrics collection
   - Performance comparison

4. **Example 04 (Jupyter)**:
   - Convert to notebook
   - Visualize metrics
   - Interactive exploration

### Implementation Tips

**Example 03 - Conversations**:
```python
# Pattern to demonstrate
history = [
    SystemMessage(content="You are a helpful Python tutor"),
    HumanMessage(content="What is Python?"),
]

response = llm.invoke(history)
history.append(AIMessage(content=response.content))

# Next turn uses previous context
history.append(HumanMessage(content="What are its main uses?"))
response = llm.invoke(history)
```

**Example 04 - Callbacks**:
```python
# Pattern to demonstrate
class TokenCounterCallback(BaseCallbackHandler):
    def __init__(self):
        self.total_tokens = 0

    def on_llm_end(self, response, **kwargs):
        if hasattr(response, "llm_output"):
            usage = response.llm_output.get("token_usage", {})
            self.total_tokens += usage.get("total_tokens", 0)

# Use with LLM
callback = TokenCounterCallback()
llm = ChatOpenAI(callbacks=[callback])
```

### Testing Strategy

**Manual Testing**:
```bash
# Test Python scripts
poetry run python examples/03_conversation.py
poetry run python examples/04_advanced.py

# Verify conversations maintain context
# Verify callbacks collect metrics
# Verify batching is faster than sequential

# Test Jupyter notebooks
poetry run jupyter notebook examples/
# Run all cells, verify output
```

**Validation Checklist**:
- [ ] Example 03 shows context retention (later questions reference earlier)
- [ ] Example 04 callbacks report metrics
- [ ] Example 04 batch is faster than sequential
- [ ] All providers work
- [ ] Error handling prevents crashes

---

## Success Criteria

### Example 03 Success

**Conversations Work**:
- [ ] 3-turn conversations with all providers
- [ ] Context clearly retained across turns
- [ ] System message affects behavior
- [ ] Later questions build on earlier responses
- [ ] History management explained clearly

**Example Output**:
```
User: What is Python?
Assistant: Python is a high-level programming language...

User: What are its main uses?  [uses context from previous answer]
Assistant: Based on what I said about Python being high-level, its main uses include...

User: How does it compare to JavaScript?  [uses context from both previous answers]
Assistant: Compared to Python which we discussed, JavaScript...
```

### Example 04 Success

**Callbacks Work**:
- [ ] Custom callback collects metrics
- [ ] Token counts reported
- [ ] Timing information captured
- [ ] Can track multiple calls
- [ ] Callback pattern explained

**Batching Works**:
- [ ] Multiple prompts processed in parallel
- [ ] Performance measured (batch vs sequential)
- [ ] Batch is noticeably faster
- [ ] When to use batching explained

**Production Patterns**:
- [ ] Error handling demonstrated
- [ ] Resource cleanup shown
- [ ] Cost tracking explained
- [ ] Best practices documented

### Code Quality

- [ ] All functions have docstrings
- [ ] Extensive comments explain WHY
- [ ] No hardcoded secrets
- [ ] Follows established patterns
- [ ] `ruff check examples/` passes

### Notebooks Work

- [ ] All cells execute
- [ ] Output preserved
- [ ] Markdown cells explain concepts
- [ ] Interactive exploration possible

---

## Outputs of This Phase

### Files Created

```
examples/
├── 03_conversation.py       # NEW: Multi-turn conversations (~250 lines)
├── 03_conversation.ipynb    # NEW: Jupyter version (~18 cells)
├── 04_advanced.py           # NEW: Callbacks & batching (~300 lines)
└── 04_advanced.ipynb        # NEW: Jupyter version (~23 cells)
```

### Complete Example Suite

**All Examples Now Exist**:
- 01_basic.py + .ipynb (basic invocation)
- 02_streaming.py + .ipynb (streaming responses)
- 03_conversation.py + .ipynb (message history)
- 04_advanced.py + .ipynb (production features)

**Learning Path Complete**: Beginner → Intermediate → Advanced

---

## Common Issues & Solutions

**Issue**: Message history grows too large
**Solution**: Show truncation/summarization patterns in comments

**Issue**: Callbacks not called
**Solution**: Verify callback passed to LLM constructor: `ChatOpenAI(callbacks=[cb])`

**Issue**: Batch vs sequential timing similar
**Solution**: Use more prompts (10+) to show clear difference

**Issue**: Token usage not available
**Solution**: Some providers don't return usage, explain in comments

**Issue**: Context not retained
**Solution**: Verify AIMessage with response content appended to history

---

## Transition to Next Phase

### Ready for Phase 06 When

**All Examples Complete**:
- [ ] Examples 01-04 all working
- [ ] All have Python + Jupyter versions
- [ ] Progressive complexity demonstrated
- [ ] All manual tests pass

**Example Suite Validated**:
- [ ] Can run all from project root
- [ ] Can run all from examples/ directory
- [ ] All show expected output
- [ ] Error handling works

**What's Next** (Phase 06):
- Write comprehensive README
- Document all examples
- Installation instructions
- Troubleshooting guide
- Complete user-facing documentation

**Why Last**:
- README documents completed work
- Can include actual example output
- Can reference all existing files
- Finalizes the template

---

## Related Documents

**Requirements**:
- [001-functional-requirements.md](../requirements/001-functional-requirements.md) - Example requirements

**Designs**:
- [004-examples-design.md](../designs/004-examples-design.md) - Example patterns

**Tasks**:
- [task-013-implement-examples-03-04-with-notebooks.md](../tasks/task-013-implement-examples-03-04-with-notebooks.md)

**Previous/Next**:
- [phase-04-basic-examples.md](phase-04-basic-examples.md) - Previous
- [phase-06-final-documentation.md](phase-06-final-documentation.md) - Next

---

## Document Metadata

- **Version**: 1.0
- **Phase Number**: 05 of 06
- **Task Range**: 012 (1 task)
- **Complexity**: Medium-High
- **Dependencies**: Phases 01-04 complete
- **Status**: Active
- **Owner**: EAD LangChain Template Team
