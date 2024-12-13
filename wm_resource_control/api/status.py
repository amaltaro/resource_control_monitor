from datetime import datetime, UTC
from flask import Blueprint, current_app, jsonify
import platform

status_bp = Blueprint('status', __name__)

@status_bp.route('/status')
def get_status():
    uptime = (datetime.now(UTC) - current_app.start_time).total_seconds()
    last_cycle = current_app.last_cycle.isoformat() if current_app.last_cycle else None

    return jsonify({
        'version': '1.0.0',
        'status': 'healthy',
        'uptime': uptime,
        'last_cycle_duration': current_app.last_cycle_duration,
        'last_cycle_start': last_cycle,
        'timestamp': datetime.now(UTC).isoformat(),
        'python_version': platform.python_version()
    }) 