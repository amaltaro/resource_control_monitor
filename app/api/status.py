from datetime import datetime
from flask import Blueprint, current_app, jsonify
import platform

status_bp = Blueprint('status', __name__)

@status_bp.route('/status')
def get_status():
    uptime = (datetime.utcnow() - current_app.start_time).total_seconds()
    last_cycle = current_app.last_cycle.isoformat() if current_app.last_cycle else None
    
    return jsonify({
        'version': '1.0.0',
        'status': 'healthy',
        'uptime': uptime,
        'last_cycle_duration': current_app.last_cycle_duration,
        'last_cycle_start': last_cycle,
        'timestamp': datetime.utcnow().isoformat(),
        'python_version': platform.python_version()
    }) 