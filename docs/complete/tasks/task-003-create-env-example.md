# Task 003: Create .env.example

## Task Context

**Phase**: 01 - Project Foundation
**Sequence**: Third task (completes Phase 01)
**Complexity**: Low-Medium
**Output**: ~150 LOC (one comprehensive template file)

### Why This Task Exists

Users need to know:
- What environment variables the project requires
- How to get API keys
- What configuration options exist
- Proper variable naming format

`.env.example` serves as both documentation and template.

### Where This Fits

```
Task 001 → Task 002 → Task 003 (YOU ARE HERE) → Task 004 → ...
Poetry     Copilot    .env.example             Interfaces
```

After this task, Phase 01 (Project Foundation) is complete.

---

## Prerequisites

### Completed Tasks

- [x] **Task 001**: Poetry project, directory structure
- [x] **Task 002**: GitHub structure, copilot-instructions.md

### Required Knowledge

**Environment Variables**:
- What `.env` files are (dotenv format)
- Difference between `.env` (secret, gitignored) and `.env.example` (template, committed)
- Why namespace variables (`EADLANGCHAIN_*`)

**Configuration**:
- What API keys are needed (OpenAI, Anthropic, Gemini)
- Optional vs required variables
- Default values

---

## Research Required

### Environment Variable Conventions

**Read**:
- `.github/copilot-instructions.md` (just created in Task 002)
- `docs/complete/requirements/003-environment-conventions.md`

**Key Patterns**:
```bash
EADLANGCHAIN_<TYPE>_<KEY>

Types:
- AI: AI provider configuration
- LOG: Logging configuration
```

### Provider Documentation

**Research API Key Locations**:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys
- Google Gemini: https://aistudio.google.com/app/apikey

---

## Code to Explore

### Reference Documents

**Pattern Reference**:
From `requirements/003-environment-conventions.md`:
```bash
# Pattern
EADLANGCHAIN_<TYPE>_<KEY>=value

# Examples
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...
EADLANGCHAIN_LOG_LEVEL=INFO
```

### Similar .env.example Files

Study other projects' .env.example files for structure ideas (good section headers, helpful comments).

---

## Task Description

### Objective

Create a comprehensive `.env.example` file that documents all environment variables, provides helpful comments, includes links to get API keys, and serves as a template for users.

### Requirements

#### File Structure

```bash
# ============================================================================
# Project Title - Environment Configuration Template
# ============================================================================
#
# Copy instructions
# IMPORTANT: Never commit .env to version control
#
# ============================================================================
# Section 1: Required Variables
# ============================================================================
#
# Variable Name
# Description
# How to get it
VARIABLE_NAME=example-value

# ============================================================================
# Section 2: Optional Variables
# ============================================================================
#
# Optional Variable (commented out by default)
# Description
# Default: value
# VARIABLE_NAME=example-value
```

#### Required Variables

**AI Provider API Keys** (at least one required):
```bash
# OpenAI API Key (Required for OpenAI examples)
# Sign up at: https://platform.openai.com
# Get your key: https://platform.openai.com/api-keys
# Format: Starts with sk-proj- or sk-
EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key (Required for Anthropic examples)
# Sign up at: https://console.anthropic.com
# Get your key: https://console.anthropic.com/settings/keys
# Format: Starts with sk-ant-
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Google Gemini API Key (Required for Gemini examples)
# Get your key: https://aistudio.google.com/app/apikey
# Format: Alphanumeric string
EADLANGCHAIN_AI_GEMINI_API_KEY=your-google-api-key-here
```

#### Optional Variables

**Logging Configuration**:
```bash
# Logging Level (Default: INFO)
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Set to desired level - shown here with default value
EADLANGCHAIN_LOG_LEVEL=INFO

# Log File Path (Default: console only)
# Uncomment to write logs to file (creates directory if needed)
# EADLANGCHAIN_LOG_FILE=logs/app.log
```

**Model Overrides** (optional):
```bash
# Override default OpenAI model (Default: gpt-4.1-nano)
# EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o

# Override default Anthropic model (Default: claude-3-5-haiku-20241022)
# EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Override default Gemini model (Default: gemini-2.5-flash-lite)
# EADLANGCHAIN_AI_GEMINI_MODEL=gemini-2.5-pro
```

#### Header Section

```bash
# ============================================================================
# EAD LangChain Template - Environment Configuration Template
# ============================================================================
#
# Copy this file to .env and fill in your API keys:
#   cp .env.example .env
#
# Then edit .env with your actual values.
#
# IMPORTANT: Never commit .env to version control!
# The .env file contains secrets and is in .gitignore
#
# ============================================================================
```

### Constraints

- Must follow `EADLANGCHAIN_<TYPE>_<KEY>` pattern exactly
- Include helpful comments for every variable
- Provide links to get API keys
- Show example/placeholder values
- Optional variables commented out by default
- Clear section separators (====lines)
- Total length: ~100-150 lines

---

## Success Criteria

### Functional

- [ ] `.env.example` exists at project root
- [ ] All required variables documented
- [ ] All optional variables documented
- [ ] Links to get API keys included
- [ ] Copy instructions in header

### Quality

- [ ] Clear section headers
- [ ] Helpful comments for each variable
- [ ] Example values shown
- [ ] Optional variables commented out
- [ ] Follows naming convention exactly
- [ ] No actual secrets (only placeholders)

### Integration

- [ ] Can copy to `.env`: `cp .env.example .env`
- [ ] Variables match what code expects
- [ ] All providers covered
- [ ] Logging configuration covered

---

## Expected Approach (Ideal Path)

### Step 1: Create File

```bash
# From project root
touch .env.example
```

### Step 2: Write Header

```bash
# ============================================================================
# EAD LangChain Template - Environment Configuration Template
# ============================================================================
#
# Copy this file to .env and fill in your API keys:
#   cp .env.example .env
#
# Then edit .env with your actual values.
#
# IMPORTANT: Never commit .env to version control!
# The .env file contains secrets and is in .gitignore.
#
# ============================================================================
```

### Step 3: Add Required AI Provider Keys

```bash
# ============================================================================
# AI Provider API Keys (at least one required)
# ============================================================================

# OpenAI API Key (Required for OpenAI examples)
# Sign up at: https://platform.openai.com
# Get your key: https://platform.openai.com/api-keys
# Format: Starts with sk-proj- or sk-
EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key (Required for Anthropic examples)
# Sign up at: https://console.anthropic.com
# Get your key: https://console.anthropic.com/settings/keys
# Format: Starts with sk-ant-
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Google Gemini API Key (Required for Gemini examples)
# Get your key: https://aistudio.google.com/app/apikey
# Format: Alphanumeric string
EADLANGCHAIN_AI_GEMINI_API_KEY=your-google-api-key-here
```

### Step 4: Add Optional Configuration

```bash
# ============================================================================
# Optional Configuration
# ============================================================================

# Logging Level (Default: INFO)
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Set to desired level - shown here with default value
EADLANGCHAIN_LOG_LEVEL=INFO

# Log File Path (Default: console only)
# Uncomment to write logs to file (creates directory if needed)
# EADLANGCHAIN_LOG_FILE=logs/app.log
```

### Step 5: Add Model Overrides

```bash
# ============================================================================
# Model Overrides (Optional - examples have defaults)
# ============================================================================

# Override default OpenAI model (Default: gpt-4.1-nano)
# EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o

# Override default Anthropic model (Default: claude-3-5-haiku-20241022)
# EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Override default Gemini model (Default: gemini-2.5-flash-lite)
# EADLANGCHAIN_AI_GEMINI_MODEL=gemini-2.5-pro
```

### Step 6: Validate

```bash
# Check file exists
ls -la .env.example

# Count lines (should be ~100-150)
wc -l .env.example

# Verify all variables use EADLANGCHAIN_ prefix
grep -v "^#" .env.example | grep -v "^$" | grep -v "EADLANGCHAIN_"
# Should output nothing (all non-comment lines have prefix)

# Verify no actual secrets
grep -i "sk-proj" .env.example
grep -i "sk-ant" .env.example
# Should only find placeholder text, not real keys
```

---

## Testing Strategy

### Validation Commands

```bash
# 1. File exists
test -f .env.example && echo "✓ .env.example exists"

# 2. Has required variables
grep -q "EADLANGCHAIN_AI_OPENAI_API_KEY" .env.example && echo "✓ OpenAI variable present"
grep -q "EADLANGCHAIN_AI_ANTHROPIC_API_KEY" .env.example && echo "✓ Anthropic variable present"
grep -q "EADLANGCHAIN_AI_GEMINI_API_KEY" .env.example && echo "✓ Gemini variable present"

# 3. Has optional variables
grep -q "EADLANGCHAIN_LOG_LEVEL" .env.example && echo "✓ Log level variable present"
grep -q "EADLANGCHAIN_LOG_FILE" .env.example && echo "✓ Log file variable present"

# 4. All variables use correct prefix
! grep -E "^[A-Z_]+=" .env.example | grep -v "EADLANGCHAIN_" && echo "✓ All variables properly prefixed"

# 5. Can be copied to .env
cp .env.example .env && echo "✓ Can copy to .env"
rm .env  # Clean up test
```

### Manual Review

- [ ] Read file start to finish
- [ ] Verify all comments are helpful
- [ ] Check links to API key pages work
- [ ] Ensure no actual secrets present
- [ ] Verify optional variables commented out

---

## Troubleshooting

### Common Issues

**Issue**: Unsure which variables to include
**Solution**: Check requirements/003-environment-conventions.md for complete list

**Issue**: Unsure what comments to write
**Solution**: Think about what a new user would need to know. Include purpose, format, how to get values.

**Issue**: Links to provider sites outdated
**Solution**: Visit each provider site, verify URL is current

**Issue**: Placeholder values look like real keys
**Solution**: Use obviously fake values like "your-api-key-here", not realistic-looking strings

---

## Output Example

### Complete .env.example (trimmed for space)

```bash
# ============================================================================
# EAD LangChain Template - Environment Configuration Template
# ============================================================================
#
# Copy this file to .env and fill in your API keys:
#   cp .env.example .env
#
# IMPORTANT: Never commit .env to version control!
#
# ============================================================================
# AI Provider API Keys (at least one required)
# ============================================================================

# OpenAI API Key
# Get yours at: https://platform.openai.com/api-keys
EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here

[... rest of variables ...]
```

---

## Next Steps

After completing this task:

1. **Commit Your Work**:
   ```bash
   git add .env.example
   git commit -m "Add environment variable template"
   ```

2. **Phase 01 Complete**:
   - Project structure: ✓
   - GitHub configuration: ✓
   - Environment template: ✓
   - Ready for Phase 02 (core utilities)

3. **Move to Task 004**:
   - Create interfaces
   - Implement configuration module
   - Begin writing actual code

---

## Related Documents

**Requirements**:
- [003-environment-conventions.md](../requirements/003-environment-conventions.md) - Complete env var specification

**Phase**:
- [phase-01-project-foundation.md](../phases/phase-01-project-foundation.md)

**Previous/Next**:
- [task-002-setup-github-write-copilot-instructions.md](task-002-setup-github-write-copilot-instructions.md) - Previous
- [task-004-create-interfaces-implement-config.md](task-004-create-interfaces-implement-config.md) - Next

---

## Document Metadata

- **Task ID**: 003
- **Phase**: 01 - Project Foundation (final task of phase)
- **Complexity**: Low-Medium
- **LOC Output**: ~100-150 lines
- **Prerequisites**: Tasks 001-002 complete
- **Validates**: Users know what configuration is needed
