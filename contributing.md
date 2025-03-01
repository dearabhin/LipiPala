# Contributing to LipiPala AI

Thank you for your interest in contributing to LipiPala AI! We're excited to welcome you to our community dedicated to preserving endangered Indian languages. This document provides guidelines and information to help make your contribution process smooth and effective.

## 🌱 Our Philosophy

LipiPala AI is built on principles of:
- **Community-centered development**: Indigenous communities lead the way
- **Ethical AI**: Respecting cultural ownership and data sovereignty
- **Accessibility**: Creating tools usable by communities with varying technical resources
- **Knowledge sharing**: Building capacity within communities

## 🛤️ Ways to Contribute

There are many ways to contribute to LipiPala AI:

### 📝 Code Contributions
- Implement new features
- Fix bugs
- Improve performance
- Add tests
- Enhance documentation

### 🗣️ Language Contributions
- Help with language documentation
- Contribute recordings or transcriptions
- Assist with linguistic analysis
- Review language-specific components

### 🎨 Design Contributions
- User interface design
- User experience improvements
- Graphic design
- Accessibility enhancements

### 📚 Documentation
- Improve existing documentation
- Translate documentation
- Create tutorials or guides
- Document use cases

### 🔍 Community Outreach
- Connecting with indigenous communities
- Partnership development
- Community engagement
- Education and awareness

## 🚀 Getting Started

### Setting Up Your Development Environment

```bash
# Clone the repository
git clone https://github.com/lipipalai/lipipalai.git
cd lipipalai

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Finding Issues to Work On

- Check out our [Issues](https://github.com/lipipalai/lipipalai/issues) page
- Look for issues labeled `good-first-issue` or `help-wanted`
- Join our community discussions to find areas where help is needed

## 📋 Contribution Process

### 1. Choose or Create an Issue

Before starting work, make sure there's an issue describing the feature/bug/improvement:
- Search existing issues to see if your idea has been discussed
- If not, create a new issue describing what you'd like to work on
- Wait for maintainer feedback before investing significant time

### 2. Fork and Clone

- Fork the repository to your GitHub account
- Clone your fork locally
- Add the upstream repository:
  ```bash
  git remote add upstream https://github.com/lipipalai/lipipalai.git
  ```

### 3. Create a Branch

Create a branch with a descriptive name:
```bash
git checkout -b feature/add-gondi-support
# or
git checkout -b fix/speech-recognition-accuracy
```

### 4. Make Your Changes

- Follow the coding style and conventions used in the project
- Write meaningful commit messages
- Add or update tests as necessary
- Update documentation to reflect your changes

### 5. Keep Your Branch Updated

Regularly sync your branch with the upstream main:
```bash
git pull upstream main
git push origin your-branch-name
```

### 6. Submit a Pull Request

When your changes are ready:
1. Push your branch to your fork
2. Create a Pull Request from your fork to the main repository
3. Fill out the PR template with details about your changes
4. Link the PR to the relevant issue

### 7. Code Review

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR

## 🧪 Testing

We value well-tested code:
- Run existing tests before submitting: `pytest`
- Add tests for new functionality
- Ensure all tests pass locally before submitting your PR

## 📏 Coding Standards

- Follow PEP 8 for Python code
- Use descriptive variable, function, and class names
- Comment your code, especially complex sections
- Document functions, classes, and modules

## 🔤 Language Documentation Standards

When contributing language resources:
- Include metadata (dialect, region, speaker demographics if available)
- Follow ISO 639 language codes when applicable
- Document pronunciation guidelines
- Respect traditional knowledge protocols of the community

## 🌐 Community Guidelines

- Be respectful and inclusive in all interactions
- Value indigenous knowledge and leadership
- Engage constructively in discussions
- Help newcomers feel welcome
- Credit others for their work and ideas

## 🌐 Special Guidelines for Language Data

- Always obtain proper consent before recording or documenting language
- Respect indigenous data sovereignty principles
- Credit community members who contribute language data
- Follow the specific cultural protocols of each language community

## 📜 License

By contributing to LipiPala AI, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## 💬 Getting Help

- Join our [community forum](https://community.lipipalai.org) (coming soon)
- Ask questions in GitHub discussions
- Reach out to maintainers via [email](mailto:contact@lipipalai.org)

---

Thank you for helping preserve India's linguistic diversity!
