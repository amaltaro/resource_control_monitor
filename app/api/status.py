from flask import Blueprint, jsonify, current_app
from datetime import datetime
import platform

status_bp = Blueprint('status', __name__)

@status_bp.route('/status')
def get_status():
    return jsonify({
        'version': '1.0.0',
        'status': 'healthy',
        'uptime': (datetime.utcnow() - current_app.start_time).total_seconds(),
        'last_cycle_duration': current_app.last_cycle_duration,
        'last_cycle_start': current_app.last_cycle.isoformat() if current_app.last_cycle else None,
        'timestamp': datetime.utcnow().isoformat(),
        'python_version': platform.python_version()
    }) 