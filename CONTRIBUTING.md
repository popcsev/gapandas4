# Contributing to GAPandas4

Thank you for your interest in contributing to GAPandas4! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, constructive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Python version and OS
- GAPandas4 version
- Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- A clear and descriptive title
- Detailed description of the proposed feature
- Explanation of why this enhancement would be useful
- Examples of how it would be used

### Pull Requests

1. Fork the repository
2. Create a new branch from `main` or `develop`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Write or update tests as needed
5. Ensure all tests pass
6. Update documentation if needed
7. Commit your changes following our commit message guidelines
8. Push to your fork and submit a pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Setting Up Your Development Environment

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/gapandas4.git
   cd gapandas4
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Code Style

We follow Python best practices and use automated tools to maintain code quality:

### Formatting

- **Black**: Code formatting (line length: 100)
  ```bash
  black gapandas4 tests
  ```

- **isort**: Import sorting
  ```bash
  isort gapandas4 tests
  ```

### Linting

- **Flake8**: Code linting
  ```bash
  flake8 gapandas4 tests
  ```

- **mypy**: Type checking
  ```bash
  mypy gapandas4
  ```

### Running All Quality Checks

```bash
# Format code
black gapandas4 tests
isort gapandas4 tests

# Check code quality
flake8 gapandas4 tests
mypy gapandas4
```

## Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=gapandas4 --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_gapandas4.py
```

Run specific test:
```bash
pytest tests/test_gapandas4.py::TestExceptions::test_base_exception
```

### Writing Tests

- Write tests for all new features and bug fixes
- Aim for high test coverage (target: 90%+)
- Use descriptive test names that explain what is being tested
- Follow the existing test structure and patterns
- Use mocks for external API calls

Example test structure:
```python
class TestYourFeature:
    """Test your new feature."""

    def test_specific_behavior(self):
        """Test that specific behavior works correctly."""
        # Arrange
        input_data = "test"

        # Act
        result = your_function(input_data)

        # Assert
        assert result == expected_output
```

## Documentation

- Update docstrings for any modified functions or classes
- Follow Google-style docstrings format
- Include examples in docstrings where helpful
- Update README.md if adding new features
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format

### Docstring Example

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When this error occurs

    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests when relevant

Example:
```
Add input validation for property IDs

- Validate property ID format before API calls
- Raise InvalidPropertyIDError for invalid formats
- Add tests for validation logic

Fixes #123
```

## Versioning

We use [Semantic Versioning](https://semver.org/):

- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward-compatible manner
- PATCH version for backward-compatible bug fixes

## Release Process

1. Update version in `setup.py` and `gapandas4/__init__.py`
2. Update CHANGELOG.md
3. Create a pull request with the version bump
4. After merge, create a GitHub release with tag `vX.Y.Z`
5. GitHub Actions will automatically build and publish to PyPI

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
