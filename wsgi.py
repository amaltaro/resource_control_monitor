"""
Provides the WSGI application entry point
Handles reverse proxy configuration
Supports both development and production environments
Maintains separation between application logic and server configuration
"""
from app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix

# Create Flask application instance using the factory pattern
app = create_app('config/settings.ini')

# Add ProxyFix middleware to handle reverse proxy headers
# x_proto=1: Trusts first X-Forwarded-Proto header (for HTTPS detection)
# x_host=1: Trusts first X-Forwarded-Host header (for hostname detection)
# Essential for proper URL generation and security in production
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Development server configuration
# Enables debug mode for development (auto-reload, detailed errors)
if __name__ == '__main__':
    app.run(debug=True) 