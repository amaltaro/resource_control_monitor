# Workload Management Resource Control Monitor

[![Tests](https://github.com/amaltaro/resource_control_monitor/actions/workflows/tests.yml/badge.svg)](https://github.com/amaltaro/resource_control_monitor/actions/workflows/tests.yml)
[![Static Analysis](https://github.com/amaltaro/resource_control_monitor/actions/workflows/static-analysis.yml/badge.svg)](https://github.com/amaltaro/resource_control_monitor/actions/workflows/static-analysis.yml)

A Flask-based monitoring service that provides real-time metrics and status information for workload management resources. The service is designed to be horizontally scalable, memory-efficient, and production-ready.

## Functionality

The WM Resource Control Monitor provides:
- Real-time system status monitoring
- Prometheus-compatible metrics endpoint
- RESTful API architecture
- Secure access control via X.509 certificates
- Compressed data transfer for efficient communication
- Configurable logging and monitoring

## API Endpoints

- `/wm_resource_monitor` - Service information and documentation
- `/wm_resource_monitor/api` - API index and endpoint listing
- `/wm_resource_monitor/api/status` - System status, version, uptime, and health information
- `/wm_resource_monitor/api/metrics` - Prometheus-compatible metrics endpoint

## Technical Capabilities

- **Performance**:
  - Supports 500 requests/second
  - Horizontally scalable architecture
  - Optimized memory footprint
  - Compressed data transfer

- **Security**:
  - X.509 certificate-based authentication
  - Role-based access control
  - Secure communication protocols

- **Monitoring**:
  - Prometheus metrics integration
  - Detailed system status reporting
  - Comprehensive logging system
  - Real-time performance metrics

## Architecture

### Components
- Flask web framework (Python 3.11+)
- SQLite3 database backend
- Gunicorn WSGI HTTP Server
- Prometheus metrics integration
- Flask-Compress for data compression

### Directory Structure
```
project_root/
├── .github/
│   └── workflows/
│       ├── static-analysis.yml
│       ├── tests.yml
│       └── release-notes.yml
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── status.py
│   │   └── metrics.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── x509.py
│   └── config/
│       └── settings.ini
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── api_t/
│   │   ├── __init__.py
│   │   └── status_t.py
│   └── auth_t/
│       ├── __init__.py
│       └── x509_t.py
├── logs/
├── pyproject.toml
├── poetry.lock
├── README.md
└── wsgi.py
```

### Prerequisites
- Python 3.11 or higher
- Poetry (dependency management)

### Development Environment

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install project dependencies:
```bash
poetry install
```

3. Run development server:
```bash
poetry run python wsgi.py
```

### Production Environment

1. Install production dependencies only:
```bash
poetry install --only main
```

2. Configure settings in `src/config/settings.ini`

3. Run with Gunicorn:
```bash
poetry run gunicorn --workers 4 \
         --worker-class gthread \
         --threads 2 \
         --bind 0.0.0.0:5000 \
         --certfile /path/to/cert.pem \
         --keyfile /path/to/key.pem \
         --ca-certs /path/to/ca.pem \
         --ssl-version TLSv1_2 \
         wsgi:app
```

### Docker Environment

1. Create a Dockerfile:
```dockerfile
FROM python:3.12-slim

# Install Poetry
RUN pip install poetry

WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies (production only)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY . .

# Run the application
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

2. Build and run:
```bash
docker build -t wm-resource-monitor .
docker run -d \
  -p 5000:5000 \
  -v /path/to/certs:/etc/certs \
  -v /path/to/logs:/var/log/app \
  wm-resource-monitor
```

### Development Tools

The project includes several development tools configured in pyproject.toml:

- **Black** (Code formatting):
```bash
poetry run black .
```

- **Ruff** (Fast linting, import sorting, and more):
```bash
# Check your code
poetry run ruff check .

# Fix auto-fixable issues
poetry run ruff check --fix .

# Format imports
poetry run ruff format .
```

- **MyPy** (Type checking):
```bash
poetry run mypy .
```

- **Pytest** (Testing):
```bash
poetry run pytest
```

- **Testing**

Run the test suite:
```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov

# Run specific test file
poetry run pytest tests/api_t/status_t.py
```

Test files are organized as:
- `tests/api_t/`: Tests for API endpoints
- `tests/auth_t/`: Tests for authentication
- `tests/integration_t/`: Integration tests
- `conftest.py`: Test fixtures and configuration

Both directories and files use the suffix `_t` (e.g., `api_t/endpoints_t.py`)

### Continuous Integration

The project uses GitHub Actions for automated checks:

- **Static Analysis**: Runs on every commit and pull request
  - Ruff static code analysis
  - Runs against Python 3.11 and 3.12
  - Cached dependencies for faster execution

To run the same checks locally:
```bash
# Run all checks
poetry run ruff check .
# poetry run ruff format --check .

# Auto-fix issues
poetry run ruff check --fix .
# poetry run ruff format .
```

### Dependency Management

- Add a new dependency:
```bash
poetry add package_name
```

- Add a development dependency:
```bash
poetry add --group dev package_name
```

- Update dependencies:
```bash
poetry update
```

- Generate requirements.txt (if needed):
```bash
poetry export -f requirements.txt --output requirements.txt
```

## Version Management

This project uses Poetry for version management following Semantic Versioning (SemVer) and PEP 440.

### Versioning Conventions
- Python/Poetry versions follow PEP 440 (e.g., `0.1.0`)
- Git tags use 'v' prefix (e.g., `v0.1.0`)
- Version in `pyproject.toml` is the source of truth

### Version Format
- MAJOR.MINOR.PATCH (e.g., 0.1.0)
- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes (backwards compatible)

### Usage
```bash
# Show current version
poetry version

# Bump patch version (0.1.0 -> 0.1.1)
poetry version patch

# Bump minor version (0.1.0 -> 0.2.0)
poetry version minor

# Bump major version (0.1.0 -> 1.0.0)
poetry version major

# Set specific version
poetry version 1.2.3
```

The version is maintained in `pyproject.toml` and serves as the single source of truth for the project version.

### Release Process

Commit messages should follow the conventional commits format:
- `feat: new feature`
- `fix: bug fix`
- `chore: maintenance task`
- `docs: documentation update`
- `deps: dependency update`

1. Update version:
```bash
poetry version patch  # or minor/major
```

2. Commit the version change:
```bash
git add pyproject.toml
git commit -m "chore: bump version to v$(poetry version -s)"
```

3. Create and push a tag:
```bash
git tag v$(poetry version -s)  # Git tag includes 'v' prefix
git push origin v$(poetry version -s)
```

Note: Poetry version commands use numbers without 'v' prefix (e.g., `0.1.0`),
while Git tags and release names include the 'v' prefix (e.g., `v0.1.0`).

The GitHub Action will automatically:
- Generate release notes from commit messages
- Create a GitHub release
- Categorize changes based on conventional commit types
- Include commit hashes and authors

Release notes will be categorized as follows:
- 🚀 Features (commits starting with 'feat:')
- 🐛 Bug Fixes (commits starting with 'fix:')
- 🧰 Maintenance (commits starting with 'chore:')
- 📚 Documentation (commits starting with 'docs:')
- ⬆️ Dependencies (commits starting with 'deps:')

Example commit messages:
```bash
git commit -m "feat: add new monitoring endpoint"
git commit -m "fix: correct status response format"
git commit -m "docs: update API documentation"
git commit -m "chore: update development dependencies"
git commit -m "deps: upgrade flask to 3.0.0"
```