import pytest
from wm_resource_control import create_app
import os
import tempfile

@pytest.fixture
def app():
    """Create and configure a test application instance."""
    # Create a temp file for test config
    config_fd, config_path = tempfile.mkstemp()
    with os.fdopen(config_fd, 'w') as config_file:
        config_file.write("""
[server]
host = 127.0.0.1
port = 5000
workers = 1
compression_level = 1
max_request_size = 100MB

[security]
x509_cert_dir = /tmp/certs
allowed_roles = admin,user,reader

[logging]
level = INFO
format = %%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s
file = /tmp/test.log

[metrics]
enabled = true
endpoint = /metrics
""")

    app = create_app(config_path)
    app.config['TESTING'] = True

    yield app

    # Cleanup
    os.unlink(config_path)

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner() 