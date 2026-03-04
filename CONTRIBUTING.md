# Contributing to SmartCut Studio

Thank you for your interest in contributing to SmartCut Studio!

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Open a new issue with the `enhancement` label
2. Describe the feature in detail
3. Explain the use case and benefits

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests if available
5. Commit with clear messages: `git commit -m 'Add amazing feature'`
6. Push to your fork: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/smartcut-studio.git
cd smartcut-studio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (if any)
pip install pytest pytest-asyncio black flake8
```

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions focused and small

### Testing

Run tests with:
```bash
pytest
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

