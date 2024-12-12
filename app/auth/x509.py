from flask import request, abort
from functools import wraps
import ssl
import logging

logger = logging.getLogger(__name__)

def require_cert_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cert = request.environ.get('SSL_CLIENT_CERT')
            if not cert:
                logger.warning("No client certificate provided")
                abort(401)
            
            try:
                x509 = ssl.PEM_cert_to_DER_cert(cert)
                # Extract role from certificate subject
                # Implementation depends on your certificate structure
                role = extract_role_from_cert(x509)
                
                if role not in allowed_roles:
                    logger.warning(f"Invalid role: {role}")
                    abort(403)
                    
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Certificate validation error: {str(e)}")
                abort(401)
        return decorated_function
    return decorator

def extract_role_from_cert(cert_der):
    # Implement certificate role extraction based on your PKI structure
    pass 