# Workload Management Resource Control Monitor

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
- Flask web framework (Python 3.12)
- SQLite3 database backend
- Gunicorn WSGI HTTP Server
- Prometheus metrics integration
- Flask-Compress for data compression

### Directory Structure

project_root/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── status.py
│   │   └── metrics.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── x509.py
│   ├── templates/
│   │   └── index.html
│   └── config/
│       └── settings.ini
├── logs/
- ├── requirements.txt
+ ├── pyproject.toml
+ ├── poetry.lock
├── README.md
└── wsgi.py

### Prerequisites
- Python 3.12 or higher
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

+ ### Production Environment
+ 
+ 1. Install production dependencies only:
+ ```bash
+ poetry install --only main
+ ```
+ 
+ 2. Configure settings in `app/config/settings.ini`
+ 
+ 3. Run with Gunicorn:
+ ```bash
+ poetry run gunicorn --workers 4 \
+          --worker-class gthread \
+          --threads 2 \
+          --bind 0.0.0.0:5000 \
+          --certfile /path/to/cert.pem \
+          --keyfile /path/to/key.pem \
+          --ca-certs /path/to/ca.pem \
+          --ssl-version TLSv1_2 \
+          wsgi:app
+ ```
+ 
+ ### Docker Environment
+ 
+ 1. Create a Dockerfile:
+ ```dockerfile
+ FROM python:3.12-slim
+ 
+ # Install Poetry
+ RUN pip install poetry
+ 
+ WORKDIR /app
+ 
+ # Copy Poetry files
+ COPY pyproject.toml poetry.lock ./
+ 
+ # Install dependencies (production only)
+ RUN poetry config virtualenvs.create false \
+     && poetry install --only main --no-interaction --no-ansi
+ 
+ # Copy application code
+ COPY . .
+ 
+ # Run the application
+ CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
+ ```
+ 
+ 2. Build and run:
+ ```bash
+ docker build -t wm-resource-monitor .
+ docker run -d \
+   -p 5000:5000 \
+   -v /path/to/certs:/etc/certs \
+   -v /path/to/logs:/var/log/app \
+   wm-resource-monitor
+ ```
+ 
+ ### Development Tools
+ 
+ The project includes several development tools configured in pyproject.toml:
+ 
+ - **Black** (Code formatting):
+ ```bash
+ poetry run black .
+ ```
+ 
+ - **Flake8** (Linting):
+ ```bash
+ poetry run flake8
+ ```
+ 
+ - **MyPy** (Type checking):
+ ```bash
+ poetry run mypy .
+ ```
+ 
+ - **Pytest** (Testing):
+ ```bash
+ poetry run pytest
+ ```
+ 
+ ### Dependency Management
+ 
+ - Add a new dependency:
+ ```bash
+ poetry add package_name
+ ```
+ 
+ - Add a development dependency:
+ ```bash
+ poetry add --group dev package_name
+ ```
+ 
+ - Update dependencies:
+ ```bash
+ poetry update
+ ```
+ 
+ - Generate requirements.txt (if needed):
+ ```bash
+ poetry export -f requirements.txt --output requirements.txt
+ ```
