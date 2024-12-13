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

            # Strip any leading/trailing whitespace from the certificate
            cert = cert.strip()

            try:
                cert_der = ssl.PEM_cert_to_DER_cert(cert)
            except Exception as e:
                logger.error(f"Failed to convert PEM to DER: {str(e)}")
                abort(401)

            try:
                role = extract_role_from_cert(cert_der)

                if role not in allowed_roles:
                    logger.warning(f"Role '{role}' not in allowed roles: {allowed_roles}")
                    abort(403)

                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Role validation error: {str(e)}")
                abort(403)

        return decorated_function
    return decorator

def extract_role_from_cert(cert_der):
    # Implement certificate role extraction based on your PKI structure
    pass 