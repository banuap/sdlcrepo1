"""
Test file for Hello World API
Tests the API endpoints to ensure they return correct responses.
"""
import sys
import json
from app import app


def test_hello_endpoint():
    """Test the /hello endpoint"""
    
    client = app.test_client()
    response = client.get('/hello')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert 'message' in data, "Response should contain 'message' field"
    assert data['message'] == 'Hello World!', "Message should be 'Hello World!'"
    assert data['status'] == 'success', "Status should be 'success'"


def test_home_endpoint():
    """Test the home endpoint"""
    client = app.test_client()
    response = client.get('/')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert 'api' in data, "Response should contain 'api' field"
    assert 'version' in data, "Response should contain 'version' field"
    assert 'endpoints' in data, "Response should contain 'endpoints' field"


if __name__ == "__main__":
    try:
        test_hello_endpoint()
        print("✓ test_hello_endpoint passed")
        
        test_home_endpoint()
        print("✓ test_home_endpoint passed")
        
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        sys.exit(1)
