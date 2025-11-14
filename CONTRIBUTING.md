# Contributing to Care MCP Server

Thank you for your interest in contributing to the Care MCP Server! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Code Style](#code-style)
7. [Submitting Changes](#submitting-changes)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/care_mcp_server.git
   cd care_mcp_server
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/yash-learner/care_mcp_server.git
   ```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Create a `.env` file for testing:
   ```bash
   cp .env.example .env
   # Edit .env with test credentials if available
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-operation` - New features
- `fix/auth-token-refresh` - Bug fixes
- `docs/update-readme` - Documentation updates
- `test/add-schema-parser-tests` - Test additions

### Commit Messages

Follow the conventional commits format:
- `feat: add support for patient management operations`
- `fix: resolve token refresh issue`
- `docs: update installation instructions`
- `test: add tests for whitelist manager`
- `refactor: improve schema parser error handling`
- `chore: update dependencies`

### Code Organization

- **config.py**: Configuration management
- **auth.py**: Authentication and token handling
- **schema_parser.py**: OpenAPI schema parsing
- **whitelist.py**: Operation filtering
- **enhancements.py**: AI-friendly metadata
- **tool_generator.py**: MCP tool generation
- **__main__.py**: Entry point and initialization

## Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_config.py
```

Run with coverage:
```bash
pytest --cov=care_mcp_server --cov-report=html
```

Run verbose:
```bash
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

Example test:
```python
def test_whitelist_blocks_destroy_operations():
    """Test that destroy operations are blocked."""
    # Arrange
    manager = WhitelistManager()
    
    # Act
    result = manager.is_allowed("facility_destroy")
    
    # Assert
    assert result is False
```

### Test Coverage Goals

- Aim for >80% code coverage
- Test happy paths and edge cases
- Test error handling
- Test integration between modules

## Code Style

### Formatting

We use Black for code formatting:
```bash
black src/ tests/
```

Check formatting without changes:
```bash
black --check src/ tests/
```

### Linting

We use Ruff for linting:
```bash
ruff check src/ tests/
```

Auto-fix issues:
```bash
ruff check --fix src/ tests/
```

### Style Guidelines

- Line length: 100 characters
- Use type hints for function signatures
- Use docstrings for modules, classes, and functions
- Follow PEP 8 conventions
- Use meaningful variable names

Example:
```python
def parse_operation(operation_id: str) -> Optional[Dict[str, Any]]:
    """
    Parse an operation from the schema.
    
    Args:
        operation_id: The operation identifier
        
    Returns:
        Operation dictionary or None if not found
    """
    # Implementation here
```

## Submitting Changes

### Pull Request Process

1. Update your fork:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub:
   - Use a descriptive title
   - Reference related issues
   - Describe what changed and why
   - Include screenshots for UI changes
   - List any breaking changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## Areas for Contribution

### High Priority

- Additional operation enhancements
- More comprehensive tests
- Integration tests with live API
- Performance optimizations
- Better error messages

### Documentation

- Tutorial videos
- More usage examples
- API reference documentation
- Deployment guides
- Troubleshooting guides

### Features

- Support for additional Care API endpoints
- Custom whitelist management UI
- Enhanced logging and monitoring
- Configuration validation
- CLI commands for common tasks

### Bug Fixes

- Check the [Issues](https://github.com/yash-learner/care_mcp_server/issues) page
- Look for issues labeled "good first issue"
- Report bugs with detailed reproduction steps

## Development Tips

### Local Testing

Test the server locally:
```bash
# Set environment variables
export CARE_USERNAME=test_user
export CARE_PASSWORD=test_pass

# Run the server
python -m care_mcp_server
```

### Debugging

Add debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### IDE Setup

**VS Code**:
- Install Python extension
- Enable format on save
- Configure pytest for test discovery

**PyCharm**:
- Mark `src/` as sources root
- Configure Black as file watcher
- Enable pytest as test runner

## Questions?

- Open an issue for questions
- Join discussions on GitHub
- Check existing issues and PRs

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.txt
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to Care MCP Server! 🎉
