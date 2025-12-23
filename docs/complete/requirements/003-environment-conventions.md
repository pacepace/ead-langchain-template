# Requirements 003: Environment Conventions

## Document Purpose

This document defines the complete environment variable strategy for the EAD LangChain Template. It establishes naming conventions, usage patterns, and best practices for configuration management.

---

## EC-001: Namespacing Strategy

### EC-001.1: The EADLANGCHAIN Prefix

**Requirement**: All environment variables MUST use the `EADLANGCHAIN_` prefix

**Rationale**:
- **Prevents Conflicts**: Avoids collisions with system-wide variables (e.g., `OPENAI_API_KEY`)
- **Clear Ownership**: Immediately identifies variables belonging to this project
- **Professional Pattern**: Follows enterprise best practices
- **Grep-able**: Easy to find all project variables: `env | grep EADLANGCHAIN`
- **Portable**: No assumptions about global environment state

**Non-Compliant Examples** (DO NOT USE):
```bash
OPENAI_API_KEY=sk-...          # Too generic
API_KEY=sk-...                  # Way too generic
PROJECT_OPENAI_KEY=sk-...       # Inconsistent prefix
```

**Compliant Examples**:
```bash
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...
EADLANGCHAIN_LOG_LEVEL=INFO
EADLANGCHAIN_AI_GEMINI_API_KEY=...
```

**Acceptance Criteria**:
- [ ] All project env vars start with `EADLANGCHAIN_`
- [ ] No exceptions to this rule
- [ ] Documented in all code and examples
- [ ] Enforced in code (ConfigError if using wrong names)

---

## EC-002: Variable Structure

### EC-002.1: Three-Part Naming Pattern

**Pattern**: `EADLANGCHAIN_<TYPE>_<KEY>`

**Components**:
1. **PREFIX**: `EADLANGCHAIN` - Project identifier (constant)
2. **TYPE**: Category/domain (AI, LOG, DB, APP, etc.)
3. **KEY**: Specific configuration item (OPENAI_API_KEY, LEVEL, etc.)

**Separator**: Underscore (`_`) between all components

**Case**: UPPER_CASE for all parts (standard Unix convention)

### EC-002.2: TYPE Categories

#### AI - AI Provider Configuration
**Purpose**: LLM provider API keys and settings

**Variables**:
```bash
# API Keys (required for each provider you want to use)
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=sk-ant-...
EADLANGCHAIN_AI_GEMINI_API_KEY=...

# Model Overrides (optional - examples have their own defaults)
EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o
EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
EADLANGCHAIN_AI_GEMINI_MODEL=gemini-2.0-flash-exp

# Provider Settings (future - not currently used)
EADLANGCHAIN_AI_TEMPERATURE=0.7
EADLANGCHAIN_AI_MAX_TOKENS=1000
```

**Acceptance Criteria**:
- [ ] All AI-related vars use `EADLANGCHAIN_AI_` prefix
- [ ] API keys for all three providers supported
- [ ] Model names are valid for respective providers
- [ ] Optional settings have sensible defaults

#### LOG - Logging Configuration
**Purpose**: Control logging behavior

**Variables**:
```bash
# Log Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
EADLANGCHAIN_LOG_LEVEL=INFO

# Log File Path (optional - logs to console if not set)
EADLANGCHAIN_LOG_FILE=logs/app.log

# Log Format (optional - uses default if not set)
EADLANGCHAIN_LOG_FORMAT="%(levelname)s - %(message)s"
```

**Acceptance Criteria**:
- [ ] All logging vars use `EADLANGCHAIN_LOG_` prefix
- [ ] Valid log levels accepted (case insensitive)
- [ ] Log file path creates parent directories if needed
- [ ] Custom format supported but not required

#### DB - Database Configuration (Future)
**Purpose**: Database connection settings (not currently implemented)

**Reserved Variables**:
```bash
EADLANGCHAIN_DB_CONNECTION_STRING=postgresql://...
EADLANGCHAIN_DB_POOL_SIZE=10
EADLANGCHAIN_DB_TIMEOUT=30
```

**Status**: Reserved for future use, not implemented yet

#### APP - Application Settings (Future)
**Purpose**: General application configuration (not currently implemented)

**Reserved Variables**:
```bash
EADLANGCHAIN_APP_NAME="My LangChain App"
EADLANGCHAIN_APP_VERSION=1.0.0
EADLANGCHAIN_APP_ENV=development
```

**Status**: Reserved for future use, not implemented yet

### EC-002.3: KEY Naming Rules

**Rules**:
1. Use UPPER_CASE for all keys
2. Separate words with underscores
3. Be descriptive but concise
4. Follow domain conventions (e.g., `API_KEY` not `KEY`)
5. Avoid abbreviations unless universally understood (OK: API, HTTP, DB; Not OK: MSG, TMP)

**Good Examples**:
```bash
EADLANGCHAIN_AI_OPENAI_API_KEY
EADLANGCHAIN_LOG_LEVEL
EADLANGCHAIN_DB_CONNECTION_STRING
```

**Bad Examples**:
```bash
EADLANGCHAIN_AI_KEY              # Not specific enough
EADLANGCHAIN_LOG_LVL             # Unnecessary abbreviation
EADLANGCHAIN_Database_String     # Mixed case
```

---

## EC-003: Environment File Management

### EC-003.1: .env File Structure

**Requirement**: Use `.env` file for local development configuration

**Location**: Project root (same directory as `pyproject.toml`)

**Format**: Standard dotenv format (KEY=VALUE pairs)

**Structure**:
```bash
# ============================================================================
# Section Header (clearly separated)
# ============================================================================

# Variable Name
# Human-readable description
# Get it from: https://example.com/link
EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here

# Another Variable
# Description here
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=your-anthropic-api-key-here

# ============================================================================
# Next Section
# ============================================================================
```

**Best Practices**:
- Group related variables under section headers
- Add comments explaining each variable
- Include links to get API keys
- Show example values in comments
- Use `your-xxx-here` as placeholder values
- Separate sections with visual dividers

**Acceptance Criteria**:
- [ ] .env file is at project root
- [ ] All required variables documented
- [ ] Clear section headers
- [ ] Helpful comments for each variable
- [ ] Links to obtain API keys
- [ ] No actual secrets committed

### EC-003.2: .env.example Template

**Requirement**: Maintain `.env.example` as documentation and template

**Purpose**:
- Serves as documentation for all environment variables
- Template for users to create their own `.env`
- Version controlled (unlike `.env`)
- Shows required vs optional variables

**Contents**:
```bash
# EAD LangChain Template - Environment Configuration Template
#
# Copy this file to .env and fill in your API keys:
#   cp .env.example .env
#
# IMPORTANT: Never commit .env to version control!

# ============================================================================
# AI Provider API Keys (at least one required)
# ============================================================================

# OpenAI API Key (Required for OpenAI examples)
# Sign up at: https://platform.openai.com
# Get your key: https://platform.openai.com/api-keys
EADLANGCHAIN_AI_OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key (Required for Anthropic examples)
# Sign up at: https://console.anthropic.com
# Get your key: https://console.anthropic.com/settings/keys
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Google Gemini API Key (Required for Gemini examples)
# Get your key: https://aistudio.google.com/app/apikey
EADLANGCHAIN_AI_GEMINI_API_KEY=your-google-api-key-here

# ============================================================================
# Optional Configuration
# ============================================================================

# Logging Level (Default: INFO)
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# EADLANGCHAIN_LOG_LEVEL=INFO

# Log File Path (Default: console only)
# Uncomment to write logs to file (creates directory if needed)
# EADLANGCHAIN_LOG_FILE=logs/app.log

# ============================================================================
# Model Overrides (Optional - examples use cost-effective defaults)
# ============================================================================
# Examples default to the most cost-effective models (gpt-5-nano,
# claude-3-haiku-20240307, gemini-2.0-flash-lite). Use these variables
# to override with higher-quality models.

# Override default OpenAI model (Default: gpt-5-nano)
# EADLANGCHAIN_AI_OPENAI_MODEL=gpt-4o

# Override default Anthropic model (Default: claude-3-haiku-20240307)
# EADLANGCHAIN_AI_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Override default Gemini model (Default: gemini-2.0-flash-lite)
# EADLANGCHAIN_AI_GEMINI_MODEL=gemini-1.5-pro
```

**Acceptance Criteria**:
- [ ] .env.example exists and is comprehensive
- [ ] All variables documented with comments
- [ ] Required variables clearly marked
- [ ] Optional variables commented out
- [ ] Links to get API keys included
- [ ] Copy instructions at top
- [ ] Default values shown in comments

### EC-003.3: .gitignore Rules

**Requirement**: Prevent committing secrets to version control

**Rules**:
```gitignore
# Environment variables - NEVER commit these
.env
.env.local
.env.*.local
*.env

# But DO commit the example template
!.env.example
```

**Acceptance Criteria**:
- [ ] .env in .gitignore
- [ ] .env.example NOT in .gitignore
- [ ] Pattern matches all .env variants
- [ ] No .env files in git history
- [ ] Warning in README about not committing .env

---

## EC-004: Loading Strategy

### EC-004.1: Automatic .env Discovery

**Requirement**: Automatically find and load .env file

**Search Strategy**:
1. Check current working directory for `.env`
2. If not found, check parent directory
3. Continue searching up the directory tree
4. Stop at project root (detected by `pyproject.toml` or `.git/`)
5. If no `.env` found anywhere, use system environment variables only

**Rationale**:
- Examples can be run from any directory
- Users don't need to specify .env path
- Works whether running from project root or subdirectory
- Graceful fallback to system env vars

**Implementation** (`config.py`):
```python
def load_env_config(env_file: Optional[str] = None) -> None:
    if env_file:
        load_dotenv(env_file)  # Explicit path provided
    else:
        # Auto-discover .env file
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            env_path = parent / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                return

        # No .env found, use system env vars
        load_dotenv()
```

**Acceptance Criteria**:
- [ ] Finds .env in project root from any subdirectory
- [ ] Works when run from `examples/`
- [ ] Works when run from `tests/`
- [ ] Works when run from project root
- [ ] Doesn't error if .env is missing
- [ ] Can override with explicit path

### EC-004.2: Loading Priority

**Requirement**: Clear order of precedence for configuration sources

**Priority** (highest to lowest):
1. **Explicit function arguments** (if supported)
2. **Environment variables** already set in shell
3. **Variables from .env file**
4. **Hardcoded defaults in code**

**Example**:
```python
# Priority demonstration
# 1. Explicit argument (highest priority)
setup_logging(level="DEBUG")

# 2. Shell environment variable
$ export EADLANGCHAIN_LOG_LEVEL=WARNING
setup_logging()  # Uses WARNING

# 3. .env file
EADLANGCHAIN_LOG_LEVEL=INFO
setup_logging()  # Uses INFO (if no shell var)

# 4. Hardcoded default (lowest priority)
setup_logging()  # Uses INFO default (if no other source)
```

**Rationale**:
- Shell vars override .env (standard dotenv behavior)
- Allows temporary overrides without editing .env
- Explicit arguments trump everything (for testing)
- Defaults provide sensible fallback

**Acceptance Criteria**:
- [ ] Shell environment variables override .env
- [ ] Function arguments override environment
- [ ] Defaults used if no other source
- [ ] Behavior is documented and consistent

### EC-004.3: Error Handling for Missing Variables

**Requirement**: Helpful errors when required variables are missing

**Error Message Template**:
```
ConfigError: API key not found for provider '{provider}'.
Please set {env_var_name} in your .env file or environment variables.
See .env.example for template.

To get an API key:
- Visit: {provider_url}
- Follow the signup/key generation process
- Add the key to your .env file
```

**Example**:
```python
# User tries to use OpenAI without API key
openai_key = get_api_key("openai")  # raises ConfigError

# Error message:
# ConfigError: API key not found for provider 'openai'.
# Please set EADLANGCHAIN_AI_OPENAI_API_KEY in your .env file or environment variables.
# See .env.example for template.
```

**Acceptance Criteria**:
- [ ] Error clearly states which provider is missing
- [ ] Error includes exact environment variable name
- [ ] Error references .env.example
- [ ] Error is user-friendly (no stack trace by default)
- [ ] Helpful for beginners

---

## EC-005: Security Best Practices

### EC-005.1: Never Hardcode Secrets

**Requirement**: Zero tolerance for hardcoded secrets

**Prohibited Patterns**:
```python
# NEVER DO THIS
api_key = "sk-1234567890abcdef"  # Hardcoded secret
openai_key = "sk-proj-..."       # Hardcoded secret
```

**Correct Pattern**:
```python
# ALWAYS DO THIS
from langchain_llm import get_api_key, load_env_config

load_env_config()
api_key = get_api_key("openai")  # From environment
```

**Acceptance Criteria**:
- [ ] No hardcoded API keys in codebase
- [ ] No hardcoded secrets in examples
- [ ] No hardcoded credentials in tests
- [ ] Code review catches hardcoded secrets
- [ ] Documentation emphasizes this rule

### EC-005.2: Logging Secrets Protection

**Requirement**: Never log API keys or sensitive data

**Safe Logging**:
```python
# Safe - doesn't log the key value
logger.info(f"Retrieved API key for provider: {provider}")
logger.debug(f"Using model: {model_name}")
```

**Unsafe Logging**:
```python
# UNSAFE - logs the actual key
logger.debug(f"API key: {api_key}")  # DON'T DO THIS
logger.info(f"Config: {get_all_api_keys()}")  # DON'T DO THIS
```

**Key Masking** (optional enhancement):
```python
def mask_key(key: str) -> str:
    """Show only first 7 chars of API key for debugging."""
    if len(key) <= 7:
        return "***"
    return f"{key[:7]}...***"

logger.debug(f"Using API key: {mask_key(api_key)}")  # OK
# Output: Using API key: sk-proj...***
```

**Acceptance Criteria**:
- [ ] No API keys logged in plain text
- [ ] Error messages don't include keys
- [ ] Debug output sanitized
- [ ] Key masking implemented for diagnostics
- [ ] Security audit confirms no leaks

### EC-005.3: .env File Permissions

**Recommendation**: Secure .env file permissions on Unix systems

**Suggested Permissions**:
```bash
chmod 600 .env   # Owner read/write only
chmod 400 .env   # Owner read only (even stricter)
```

**Rationale**:
- Prevents other users on shared systems from reading secrets
- Standard security practice
- Easy to implement

**Acceptance Criteria**:
- [ ] README recommends setting file permissions
- [ ] Documentation shows chmod command
- [ ] Works on macOS/Linux (Windows has different model)
- [ ] Optional but recommended

---

## EC-006: Development vs Production

### EC-006.1: Local Development (.env)

**Use Case**: Local development on developer machine

**Configuration**:
- Use `.env` file in project root
- One `.env` per developer (not shared)
- Contains personal API keys
- Never committed to git

**Setup**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### EC-006.2: Testing (.env.test)

**Use Case**: Running tests with mock or test API keys

**Configuration**:
- Optional `.env.test` file
- Can use pytest fixtures to set env vars
- Test keys or mocked values
- Safe to commit if no real secrets

**Setup**:
```python
# In conftest.py
@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("EADLANGCHAIN_AI_OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("EADLANGCHAIN_LOG_LEVEL", "DEBUG")
```

### EC-006.3: CI/CD (Environment Secrets)

**Use Case**: Running tests in GitHub Actions or other CI

**Configuration**:
- Use CI platform's secrets management (e.g., GitHub Secrets)
- Set as environment variables in CI config
- No .env file needed

**Example** (GitHub Actions):
```yaml
env:
  EADLANGCHAIN_AI_OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  EADLANGCHAIN_LOG_LEVEL: INFO
```

### EC-006.4: Production Deployment (Future)

**Use Case**: Deployed application (not currently in scope)

**Configuration**:
- Use platform-specific secrets management
  - AWS: Secrets Manager, Parameter Store
  - GCP: Secret Manager
  - Azure: Key Vault
  - Docker: Environment variables or secrets
- No .env files in production
- Secrets injected at runtime

**Example** (conceptual):
```python
# Production: fetch from secrets manager
# Development: use .env file
if os.getenv("ENVIRONMENT") == "production":
    api_key = fetch_from_secrets_manager("openai-key")
else:
    api_key = get_api_key("openai")
```

---

## EC-007: Validation and Debugging

### EC-007.1: Configuration Validation

**Requirement**: Provide way to check configuration without running examples

**Validation Function**:
```python
def validate_configuration() -> Dict[str, bool]:
    """
    Check which providers are configured.

    :return: Dict mapping provider names to configuration status
    :rtype: Dict[str, bool]
    """
    keys = get_all_api_keys()
    return {
        provider: (key is not None and len(key) > 0)
        for provider, key in keys.items()
    }

# Usage
status = validate_configuration()
# {'openai': True, 'anthropic': False, 'gemini': True}
```

**CLI Tool** (nice-to-have):
```bash
python -m langchain_llm.check_config

# Output:
# Configuration Status:
# ✓ OpenAI:    Configured (key starts with sk-proj...)
# ✗ Anthropic: Missing (set EADLANGCHAIN_AI_ANTHROPIC_API_KEY)
# ✓ Gemini:    Configured (key present)
```

**Acceptance Criteria**:
- [ ] Can check configuration programmatically
- [ ] Returns clear status for each provider
- [ ] Doesn't log actual keys
- [ ] Helps debug setup issues

### EC-007.2: Debug Mode

**Requirement**: Enhanced logging for troubleshooting

**Activation**:
```bash
export EADLANGCHAIN_LOG_LEVEL=DEBUG
python examples/01_basic.py
```

**Debug Output**:
```
DEBUG    2025-01-15 10:30:45 src.langchain_llm.config.load_env_config.44: Found .env file at /path/to/project/.env
DEBUG    2025-01-15 10:30:45 src.langchain_llm.config.get_api_key.75: Retrieved API key for provider: openai
DEBUG    2025-01-15 10:30:45 src.langchain_llm.config.get_api_key.80: API key starts with: sk-proj
INFO     2025-01-15 10:30:45 examples.01_basic.basic_openai_example.27: Running OpenAI example
```

**Acceptance Criteria**:
- [ ] DEBUG level shows configuration details
- [ ] Shows which .env file was loaded
- [ ] Shows which providers are configured (without keys)
- [ ] Shows model names being used
- [ ] Helps troubleshoot setup issues

---

## EC-008: Migration from Generic Names

### EC-008.1: Avoiding Generic Variables

**Problem**: Many LangChain examples use generic environment variable names

**Generic Names** (DON'T use these):
```bash
OPENAI_API_KEY=sk-...           # Used by many tools
ANTHROPIC_API_KEY=sk-ant-...    # Generic
GOOGLE_API_KEY=...              # Way too generic
```

**Why This is Bad**:
- Conflicts with other tools using same names
- Pollution of global environment
- Unclear which project uses which key
- Hard to manage multiple projects

**Our Names** (DO use these):
```bash
EADLANGCHAIN_AI_OPENAI_API_KEY=sk-...
EADLANGCHAIN_AI_ANTHROPIC_API_KEY=sk-ant-...
EADLANGCHAIN_AI_GEMINI_API_KEY=...
```

**Acceptance Criteria**:
- [ ] Never use generic variable names
- [ ] Documentation explains why
- [ ] Examples always use prefixed names
- [ ] ConfigError if trying to use generic names

### EC-008.2: Not Using Provider Defaults

**Requirement**: Explicitly pass API keys to LangChain providers

**Wrong** (relies on provider defaults):
```python
# This would look for OPENAI_API_KEY (generic)
llm = ChatOpenAI(model="gpt-4o-mini")  # NO
```

**Correct** (explicit API key):
```python
# This uses our namespaced variable
api_key = get_api_key("openai")
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)  # YES
```

**Rationale**:
- Explicit is better than implicit
- No magic environment variable lookups
- Clear which configuration is being used
- Testable (can inject mock keys)

**Acceptance Criteria**:
- [ ] All LangChain provider instantiations include explicit `api_key` parameter
- [ ] No reliance on provider default environment variable names
- [ ] Examples demonstrate explicit pattern
- [ ] Documentation emphasizes this approach

---

## EC-009: Documentation Requirements

### EC-009.1: README Environment Section

**Requirement**: README must document all environment variables

**Required Sections**:
1. **Quick Start** - How to copy .env.example
2. **Required Variables** - Which ones are needed
3. **Optional Variables** - What can be customized
4. **Getting API Keys** - Links for each provider
5. **Troubleshooting** - Common issues

### EC-009.2: Copilot Instructions

**Requirement**: AI coding assistants must follow conventions

**In .github/copilot-instructions.md**:
- Document the EADLANGCHAIN_ prefix requirement
- Explain the TYPE_KEY structure
- Provide examples
- Explain why generic names aren't used

**Enforcement**:
- AI-generated code should use prefixed variables
- Code reviews catch non-compliant code
- Enforcement tests validate

---

## EC-010: Future Extensions

### EC-010.1: Adding New Variable Types

**Process** when adding a new TYPE category:
1. Choose a clear, short TYPE name (2-5 chars)
2. Document all variables in that category
3. Update .env.example
4. Update this document (EC-002.2)
5. Add helper functions in config.py if needed
6. Update README

**Example** (adding DB type):
```bash
# 1. Choose TYPE: DB
# 2. Define variables:
EADLANGCHAIN_DB_CONNECTION_STRING=postgresql://...
EADLANGCHAIN_DB_POOL_SIZE=10

# 3. Update .env.example
# 4. Update this doc
# 5. Add to config.py:
def get_db_connection() -> str:
    return os.getenv("EADLANGCHAIN_DB_CONNECTION_STRING")

# 6. Update README
```

### EC-010.2: Provider-Specific Settings

**Future Enhancement**: Per-provider configuration beyond API keys

**Possible Variables**:
```bash
# OpenAI specific
EADLANGCHAIN_AI_OPENAI_ORG_ID=org-...
EADLANGCHAIN_AI_OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic specific
EADLANGCHAIN_AI_ANTHROPIC_VERSION=2024-01-01

# Rate limiting
EADLANGCHAIN_AI_RATE_LIMIT_RPM=60
EADLANGCHAIN_AI_RATE_LIMIT_TPM=90000
```

**Status**: Not currently implemented, reserved for future use

---

## Related Documents

- **Previous**: [002-technical-requirements.md](002-technical-requirements.md) - Tech stack
- **Next**: [004-quality-requirements.md](004-quality-requirements.md) - Testing and quality
- **See Also**:
  - [designs/002-configuration-design.md](../designs/002-configuration-design.md) - Implementation details

## Document Metadata

- **Version**: 1.0
- **Status**: Active
- **Owner**: EAD LangChain Template Team
