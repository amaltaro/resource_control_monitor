from flask import Flask, redirect, url_for, render_template
from flask_compress import Compress
from prometheus_flask_exporter import PrometheusMetrics
import configparser
import logging.config
from datetime import datetime
import os

def create_app(config_path='config/settings.ini'):
    app = Flask(__name__)
    
    # Load configuration
    config = configparser.ConfigParser()
    
    # Get absolute path to config file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(base_dir, 'app', config_path)
    
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found at: {config_file!r}")
    
    try:
        config.read(config_file)
        if not config.sections():
            raise ValueError(f"No configuration sections found in {config_file!r}")
            
        if 'logging' not in config:
            raise KeyError(f"Required 'logging' section missing from {config_file!r}")
            
        # Initialize compression
        Compress(app)
        
        # Initialize metrics
        PrometheusMetrics(app)
        
        # Setup logging
        setup_logging(config['logging'])
        
        # Track application state
        app.start_time = datetime.utcnow()
        app.last_cycle = None
        app.last_cycle_duration = None
        
        # Register blueprints
        from .api.status import status_bp
        from .api.metrics import metrics_bp
        
        app.register_blueprint(status_bp, url_prefix='/wm_resource_monitor/api')
        app.register_blueprint(metrics_bp, url_prefix='/wm_resource_monitor/api')
        
        @app.route('/wm_resource_monitor')
        def index():
            """Root route that serves the application description page"""
            return render_template('index.html')
        
        @app.route('/wm_resource_monitor/api')
        def api_index():
            """List available API endpoints"""
            return {
                'endpoints': {
                    'status': url_for('status.get_status', _external=True),
                    'metrics': url_for('metrics.metrics', _external=True)
                },
                'version': '1.0.0'
            }
        
        return app
        
    except Exception as e:
        print(f"Error initializing application: {str(e)!r}")
        print(f"Current working directory: {os.getcwd()!r}")
        print(f"Attempted config path: {config_file!r}")
        raise

def setup_logging(config):
    # Create log directory if it doesn't exist
    log_file = config['file']
    log_dir = os.path.dirname(log_file)
    
    try:
        # Create directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        # Configure logging
        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                    'format': config['format'],
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': log_file,
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'formatter': 'default',
                },
                'console': {  # Add console handler for development
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'stream': 'ext://sys.stdout'
                }
            },
            'root': {
                'level': config['level'],
                'handlers': ['file', 'console']  # Log to both file and console
            }
        })
        
        logger = logging.getLogger(__name__)
        logger.info(f"Logging initialized. Log file: {log_file}")
        
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        print(f"Attempted log file path: {log_file}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Fallback to basic console logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to setup file logging. Falling back to console logging. Error: {str(e)}") 