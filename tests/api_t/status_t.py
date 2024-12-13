from datetime import datetime
import pytest
from http import HTTPStatus

def test_status_endpoint(client):
    """Test the status endpoint returns correct data structure."""
    response = client.get('/wm_resource_monitor/api/status')
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    
    # Check required fields
    assert 'version' in data
    assert 'status' in data
    assert 'uptime' in data
    assert 'timestamp' in data
    assert 'python_version' in data
    
    # Check data types
    assert isinstance(data['uptime'], float | int)
    assert isinstance(data['timestamp'], str)
    
    # Validate timestamp format
    try:
        timestamp = datetime.fromisoformat(data['timestamp'])
        assert timestamp.tzinfo is not None  # Ensure timezone info exists
    except ValueError:
        pytest.fail("Timestamp is not in ISO format")

def test_metrics_endpoint(client):
    """Test the metrics endpoint returns Prometheus format."""
    response = client.get('/wm_resource_monitor/api/metrics')
    assert response.status_code == HTTPStatus.OK
    assert response.content_type == 'text/plain; version=0.0.4; charset=utf-8'

def test_api_index(client):
    """Test the API index returns available endpoints."""
    response = client.get('/wm_resource_monitor/api')
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    
    assert 'endpoints' in data
    assert 'status' in data['endpoints']
    assert 'metrics' in data['endpoints'] 