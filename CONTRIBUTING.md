# Contributing to HireLens

First off, thank you for considering contributing to HireLens! 🎉

This document provides guidelines and instructions for contributing. Following these guidelines helps maintain a clean, professional, and welcoming project for everyone.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Development Setup](#-development-setup)
- [Coding Standards](#-coding-standards)
- [Commit Guidelines](#-commit-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Reporting Bugs](#-reporting-bugs)
- [Suggesting Features](#-suggesting-features)
- [Community](#-community)

---

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

**Our Standards:**

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

**Unacceptable Behavior:**

- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## 🎯 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the [issue tracker](https://github.com/logiclayer0/Hire-Lens/issues) to avoid duplicates.

**When you create a bug report, include:**

- **Clear title** — Descriptive and specific
- **Steps to reproduce** — Numbered list
- **Expected behavior** — What should happen
- **Actual behavior** — What actually happens
- **Environment** — OS, Python/Node versions, browser
- **Screenshots/Logs** — If applicable

**Example template:**

```markdown
### Description
Brief description of the bug.

### Steps to Reproduce
1. Go to `/candidates`
2. Click on a candidate
3. Scroll to requirement section

### Expected Behavior
Evidence chips should expand on click.

### Actual Behavior
Evidence chips do not respond to clicks.

### Environment
- OS: Windows 11
- Python: 3.13
- Node: 20.x
- Browser: Chrome 120
```

### 💡 Suggesting Features

We welcome feature suggestions! Please open an issue with:

- **Use case** — Why is this feature needed?
- **Proposed solution** — How should it work?
- **Alternatives** — What other approaches did you consider?
- **Additional context** — Screenshots, mockups, examples

### 📝 Improving Documentation

Documentation improvements are always welcome:

- Fix typos or broken links
- Clarify ambiguous sections
- Add missing examples
- Translate to other languages

### 🔧 Code Contributions

See the [Development Setup](#-development-setup) section below to get started.

---

## 🛠️ Development Setup

### Prerequisites

- **Python** 3.13+
- **Node.js** 20+
- **Git**
- **Groq API key** ([get one free](https://console.groq.com/keys))

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Hire-Lens.git
cd Hire-Lens

# Add upstream remote
git remote add upstream https://github.com/logiclayer0/Hire-Lens.git
```

### Backend Setup

```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Run Development Servers

**Terminal 1 — Backend**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend**
```bash
cd frontend
npm run dev
```

**Terminal 3 — Seed Data**
```bash
cd scripts
python seed_data.py
```

Access:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## 📐 Coding Standards

### Python (Backend)

- **Style:** [PEP 8](https://peps.python.org/pep-0008/)
- **Type hints:** Required for all functions
- **Docstrings:** Google style
- **Max line length:** 100 characters
- **Imports:** Sorted with `isort`
- **Formatting:** `black` recommended

**Example:**

```python
def match_candidate(
    self,
    profile: CandidateProfile,
    jd: JobDescription,
) -> CandidateMatch:
    """Match a candidate against a job description.

    Args:
        profile: Structured candidate profile.
        jd: Parsed job description.

    Returns:
        Candidate match with evidence-backed scoring.
    """
    ...
```

### TypeScript (Frontend)

- **Style:** [Airbnb TypeScript](https://github.com/airbnb/javascript)
- **Strict mode:** Enabled
- **No `any`:** Use proper types
- **Components:** Functional, with hooks
- **Naming:** PascalCase for components, camelCase for functions

**Example:**

```typescript
type CandidateCardProps = {
  match: CandidateMatch;
};

export function CandidateCard({ match }: CandidateCardProps) {
  return (
    <div className="rounded-xl border border-slate-800">
      {/* ... */}
    </div>
  );
}
```

### File Naming

| Type | Convention | Example |
|------|-----------|---------|
| Python modules | snake_case | `jd_parser.py` |
| React components | PascalCase | `CandidateCard.tsx` |
| Utilities | camelCase | `formatDate.ts` |
| Constants | UPPER_SNAKE | `API_BASE_URL` |

---

## 📝 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Build, dependencies |
| `ci` | CI/CD changes |

### Examples

```bash
feat(matcher): add weighted scoring for must-have requirements

fix(extractor): handle empty resume sections gracefully

docs(readme): add architecture diagram

refactor(query): simplify vector store interface

chore(deps): bump groq to 0.13.0
```

### Rules

- Use **imperative mood** ("add" not "added")
- **Lowercase** subject line
- **No period** at end of subject
- **Max 72 characters** for subject line
- Reference issues: `Closes #42`

---

## 🔄 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/issue-description
```

**Branch naming:**
- `feat/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation
- `refactor/` — Code restructuring
- `test/` — Tests
- `chore/` — Maintenance

### 2. Make Changes

- Write clean, tested code
- Follow coding standards
- Update documentation if needed
- Add tests for new features

### 3. Test Locally

```bash
# Backend tests
cd backend
pytest -q

# Frontend build
cd frontend
npm run build
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat(scope): description"
```

### 5. Push and Open PR

```bash
git push origin feat/your-feature-name
```

Then open a Pull Request on GitHub.

### PR Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass locally
- [ ] No merge conflicts
- [ ] PR description is clear and complete

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactor
- [ ] Performance improvement

## Related Issues
Closes #123

## Testing
How did you test this?

## Screenshots
If applicable.

## Checklist
- [ ] Tests pass
- [ ] Docs updated
- [ ] No breaking changes
```

### Review Process

1. Maintainer reviews PR
2. Feedback provided within 48 hours
3. Address feedback
4. Once approved, PR is merged

---

## 🎨 UI/UX Guidelines

When contributing UI changes:

- **Follow existing design system** — Tailwind, dark theme
- **Use provided components** — `CandidateCard`, `EvidenceChip`, etc.
- **Responsive** — Test on mobile and desktop
- **Accessible** — Proper ARIA labels, keyboard navigation
- **Consistent spacing** — Use Tailwind spacing scale

### Color Palette

| Purpose | Color | Class |
|---------|-------|-------|
| Background | Dark navy | `bg-slate-950` |
| Panel | Slate | `bg-slate-900/40` |
| Accent | Indigo | `text-indigo-400` |
| Success | Emerald | `text-emerald-400` |
| Warning | Amber | `text-amber-400` |
| Error | Rose | `text-rose-400` |

---

## 🧪 Testing Guidelines

### Backend Tests

```bash
cd backend
pytest -v
pytest tests/test_matcher.py::test_scoring -v
```

### Writing Tests

- **Unit tests** for individual functions
- **Integration tests** for API endpoints
- **Mock external calls** (Groq, ChromaDB)
- **Use fixtures** for shared setup

**Example:**

```python
def test_matcher_scores_must_have_higher(sample_profile, sample_jd):
    """Must-have requirements should weigh more than nice-to-have."""
    result = matcher.match_candidate(sample_profile, sample_jd)
    assert result.overall_score > 0
    assert len(result.matched_requirements) > 0
```

---

## 📚 Documentation Standards

- Use **Markdown**
- Include **code examples** for APIs
- Keep lines under **100 characters**
- Add **table of contents** for long docs
- Update **README** for user-facing changes

---

## 🏷️ Issue Labels

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | New feature request |
| `documentation` | Docs improvement |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `priority: high` | Urgent |
| `priority: low` | Can wait |

---

## 🎓 Learning Resources

New to the stack? Check these out:

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Next.js Learn](https://nextjs.org/learn)
- [Groq Documentation](https://console.groq.com/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

## 💬 Community

- **Issues:** [GitHub Issues](https://github.com/logiclayer0/Hire-Lens/issues)
- **Discussions:** [GitHub Discussions](https://github.com/logiclayer0/Hire-Lens/discussions)

---

## 🙏 Recognition

Contributors will be:

- Listed in the README's contributors section
- Credited in release notes
- Forever appreciated ❤️

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<div align="center">

**Thank you for contributing to HireLens!** 🚀

Every contribution, no matter how small, makes a difference.

</div>
