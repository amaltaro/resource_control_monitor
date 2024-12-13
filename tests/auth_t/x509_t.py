import pytest
from src.auth.x509 import require_cert_role
from unittest.mock import Mock, patch
from flask import Flask

@pytest.fixture
def mock_app():
    app = Flask(__name__)
    return app

def test_require_cert_role_no_cert(mock_app):
    """Test authentication fails when no certificate is provided."""
    with mock_app.test_request_context() as ctx:
        mock_view = Mock()
        protected_view = require_cert_role(['admin'])(mock_view)
        
        with pytest.raises(Exception) as exc_info:
            protected_view()
        assert exc_info.value.code == 401

def test_require_cert_role_invalid_role(mock_app):
    """Test authentication fails with invalid role."""
    mock_cert_pem = """-----BEGIN CERTIFICATE-----
MIICXTCCAcYCCQC8C6nT8Y1xLjANBgkqhkiG9w0BAQUFADBzMQswCQYDVQQGEwJV
UzELMAkGA1UECAwCQ0ExFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xDTALBgNVBAoM
BFRlc3QxDTALBgNVBAsMBFRlc3QxITAfBgNVBAMMGHRlc3QuZXhhbXBsZS5jb20u
dmFsaWQwHhcNMjMwMTAxMDAwMDAwWhcNMjQwMTAxMDAwMDAwWjBzMQswCQYDVQQG
EwJVUzELMAkGA1UECAwCQ0ExFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xDTALBgNV
BAoMBFRlc3QxDTALBgNVBAsMBFRlc3QxITAfBgNVBAMMGHRlc3QuZXhhbXBsZS5j
b20udmFsaWQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBALsR45vWDRMrV6qr
kum3sdExcfJHWfqYrsLUbDekHPpjo09iMg6Qapn7aB6To/yRDDYYDT4M2NlvLWWY
GE/Emo/zIpCztDHu+obEUtkoZZByHR6jOUvr69TFmjIeseDNRVHgV1R1eurBnlSD
7rINhY7tE7RdmnkLrPljFnJjAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAaU8f
-----END CERTIFICATE-----"""

    with mock_app.test_request_context() as ctx:
        ctx.request.environ['SSL_CLIENT_CERT'] = mock_cert_pem

        mock_view = Mock()
        protected_view = require_cert_role(['admin'])(mock_view)

        # Mock both the PEM to DER conversion and role extraction
        mock_der = b'mock_der_cert'
        
        # Add debug logging to see what's happening
        def mock_pem_to_der(pem):
            print(f"Converting PEM to DER: {pem[:50]}...")
            return mock_der

        def mock_extract_role(der):
            print(f"Extracting role from DER: {der}")
            return 'user'

        with patch('ssl.PEM_cert_to_DER_cert', side_effect=mock_pem_to_der), \
             patch('src.auth.x509.extract_role_from_cert', side_effect=mock_extract_role):
            with pytest.raises(Exception) as exc_info:
                protected_view()
            print(f"Exception raised: {exc_info.value}")
            assert exc_info.value.code == 403

def test_require_cert_role_valid(mock_app):
    """Test authentication succeeds with valid certificate and role."""
    mock_cert_pem = """
    -----BEGIN CERTIFICATE-----
    MIICXTCCAcYCCQC8C6nT8Y1xLjANBgkqhkiG9w0BAQUFADBzMQswCQYDVQQGEwJV
    UzELMAkGA1UECAwCQ0ExFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xDTALBgNVBAoM
    BFRlc3QxDTALBgNVBAsMBFRlc3QxITAfBgNVBAMMGHRlc3QuZXhhbXBsZS5jb20u
    dmFsaWQwHhcNMjMwMTAxMDAwMDAwWhcNMjQwMTAxMDAwMDAwWjBzMQswCQYDVQQG
    EwJVUzELMAkGA1UECAwCQ0ExFjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xDTALBgNV
    BAoMBFRlc3QxDTALBgNVBAsMBFRlc3QxITAfBgNVBAMMGHRlc3QuZXhhbXBsZS5j
    b20udmFsaWQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBALsR45vWDRMrV6qr
    kum3sdExcfJHWfqYrsLUbDekHPpjo09iMg6Qapn7aB6To/yRDDYYDT4M2NlvLWWY
    GE/Emo/zIpCztDHu+obEUtkoZZByHR6jOUvr69TFmjIeseDNRVHgV1R1eurBnlSD
    7rINhY7tE7RdmnkLrPljFnJjAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAaU8f
    ...
    -----END CERTIFICATE-----
    """

    with mock_app.test_request_context() as ctx:
        ctx.request.environ['SSL_CLIENT_CERT'] = mock_cert_pem

        mock_view = Mock(return_value='success')
        protected_view = require_cert_role(['admin'])(mock_view)

        # Mock the extract_role_from_cert function to return admin role
        with patch('src.auth.x509.extract_role_from_cert', return_value='admin'):
            result = protected_view()
            assert result == 'success'