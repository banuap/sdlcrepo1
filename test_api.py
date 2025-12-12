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


def test_login_success():
    """Test successful login with username and password"""
    client = app.test_client()
    response = client.post('/login',
                          json={'username': 'testuser', 'password': 'testpass'},
                          content_type='application/json')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert data['status'] == 'success', "Login should be successful"
    assert 'message' in data, "Response should contain 'message' field"
    assert data['username'] == 'testuser', "Username should be returned"


def test_login_missing_data():
    """Test login with missing data"""
    client = app.test_client()
    response = client.post('/login',
                          json={},
                          content_type='application/json')
    
    assert response.status_code == 400, "Expected status code 400"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"


def test_login_missing_username():
    """Test login with missing username"""
    client = app.test_client()
    response = client.post('/login',
                          json={'password': 'testpass'},
                          content_type='application/json')
    
    assert response.status_code == 400, "Expected status code 400"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"
    assert 'Username and password are required' in data['message'], "Error message should mention required fields"


def test_login_missing_password():
    """Test login with missing password"""
    client = app.test_client()
    response = client.post('/login',
                          json={'username': 'testuser'},
                          content_type='application/json')
    
    assert response.status_code == 400, "Expected status code 400"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"
    assert 'Username and password are required' in data['message'], "Error message should mention required fields"


if __name__ == "__main__":
    try:
        test_hello_endpoint()
        print("✓ test_hello_endpoint passed")
        
        test_home_endpoint()
        print("✓ test_home_endpoint passed")
        
        test_login_success()
        print("✓ test_login_success passed")
        
        test_login_missing_data()
        print("✓ test_login_missing_data passed")
        
        test_login_missing_username()
        print("✓ test_login_missing_username passed")
        
        test_login_missing_password()
        print("✓ test_login_missing_password passed")
        
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        sys.exit(1)
