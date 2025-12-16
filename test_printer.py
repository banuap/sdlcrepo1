"""
Test file for Printer Configuration API
Tests the printer endpoints to ensure they return correct responses.
"""
import sys
import json
from app import app, printer_profiles


def test_printer_config_page():
    """Test the /printer endpoint"""
    client = app.test_client()
    response = client.get('/printer')
    
    assert response.status_code == 200, "Expected status code 200"
    assert response.content_type == 'text/html; charset=utf-8', "Response should be HTML"
    assert b'Smart Printer Configuration' in response.data, "Page should contain title"


def test_get_printer_profiles():
    """Test getting all printer profiles"""
    client = app.test_client()
    response = client.get('/printer/profiles')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert data['status'] == 'success', "Status should be success"
    assert 'profiles' in data, "Response should contain profiles"
    assert isinstance(data['profiles'], list), "Profiles should be a list"
    assert len(data['profiles']) > 0, "Should have at least one default profile"


def test_create_printer_profile():
    """Test creating a new printer profile"""
    client = app.test_client()
    
    profile_data = {
        'name': 'Test Profile',
        'paper_size': 'A4',
        'orientation': 'Landscape',
        'color_mode': 'Color',
        'quality': 'High',
        'duplex': True,
        'copies': 2,
        'is_favorite': True
    }
    
    response = client.post('/printer/profiles',
                          json=profile_data,
                          content_type='application/json')
    
    assert response.status_code == 201, "Expected status code 201"
    
    data = json.loads(response.data)
    assert data['status'] == 'success', "Status should be success"
    assert 'profile' in data, "Response should contain profile"
    assert data['profile']['name'] == 'Test Profile', "Profile name should match"
    assert data['profile']['paper_size'] == 'A4', "Paper size should match"


def test_create_profile_without_name():
    """Test creating profile without name should fail"""
    client = app.test_client()
    
    profile_data = {
        'paper_size': 'Letter'
    }
    
    response = client.post('/printer/profiles',
                          json=profile_data,
                          content_type='application/json')
    
    assert response.status_code == 400, "Expected status code 400"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"


def test_update_printer_profile():
    """Test updating a printer profile"""
    client = app.test_client()
    
    # First create a profile
    profile_data = {
        'name': 'Update Test Profile',
        'paper_size': 'Letter',
        'quality': 'Draft'
    }
    
    create_response = client.post('/printer/profiles',
                                 json=profile_data,
                                 content_type='application/json')
    
    created_profile = json.loads(create_response.data)['profile']
    profile_id = created_profile['id']
    
    # Now update it
    update_data = {
        'name': 'Updated Profile',
        'quality': 'High'
    }
    
    response = client.put(f'/printer/profiles/{profile_id}',
                         json=update_data,
                         content_type='application/json')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert data['status'] == 'success', "Status should be success"
    assert data['profile']['name'] == 'Updated Profile', "Name should be updated"
    assert data['profile']['quality'] == 'High', "Quality should be updated"


def test_update_nonexistent_profile():
    """Test updating a profile that doesn't exist"""
    client = app.test_client()
    
    response = client.put('/printer/profiles/nonexistent',
                         json={'name': 'Test'},
                         content_type='application/json')
    
    assert response.status_code == 404, "Expected status code 404"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"


def test_delete_printer_profile():
    """Test deleting a printer profile"""
    client = app.test_client()
    
    # First create a profile
    profile_data = {
        'name': 'Delete Test Profile',
        'paper_size': 'Letter'
    }
    
    create_response = client.post('/printer/profiles',
                                 json=profile_data,
                                 content_type='application/json')
    
    created_profile = json.loads(create_response.data)['profile']
    profile_id = created_profile['id']
    
    # Now delete it
    response = client.delete(f'/printer/profiles/{profile_id}')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert data['status'] == 'success', "Status should be success"


def test_delete_default_profile():
    """Test that default profile cannot be deleted"""
    client = app.test_client()
    
    response = client.delete('/printer/profiles/default')
    
    assert response.status_code == 400, "Expected status code 400"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"
    assert 'Cannot delete default profile' in data['message'], "Error message should mention default profile"


def test_delete_nonexistent_profile():
    """Test deleting a profile that doesn't exist"""
    client = app.test_client()
    
    response = client.delete('/printer/profiles/nonexistent')
    
    assert response.status_code == 404, "Expected status code 404"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"


def test_get_printer_presets():
    """Test getting printer presets"""
    client = app.test_client()
    response = client.get('/printer/presets')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert data['status'] == 'success', "Status should be success"
    assert 'presets' in data, "Response should contain presets"
    assert 'draft_documents' in data['presets'], "Should have draft_documents preset"
    assert 'photo_quality' in data['presets'], "Should have photo_quality preset"
    assert 'text_heavy' in data['presets'], "Should have text_heavy preset"


def test_generate_print_preview():
    """Test generating a print preview"""
    client = app.test_client()
    
    preview_settings = {
        'paper_size': 'Letter',
        'orientation': 'Portrait',
        'color_mode': 'Color',
        'quality': 'High',
        'duplex': True,
        'copies': 1
    }
    
    response = client.post('/printer/preview',
                          json=preview_settings,
                          content_type='application/json')
    
    assert response.status_code == 200, "Expected status code 200"
    
    data = json.loads(response.data)
    assert data['status'] == 'success', "Status should be success"
    assert 'preview' in data, "Response should contain preview"
    assert data['preview']['paper_size'] == 'Letter', "Paper size should match"
    assert data['preview']['orientation'] == 'Portrait', "Orientation should match"


def test_preview_without_data():
    """Test preview without data should fail"""
    client = app.test_client()
    
    response = client.post('/printer/preview',
                          data='',
                          content_type='application/json')
    
    assert response.status_code == 400, "Expected status code 400"
    
    data = json.loads(response.data)
    assert data['status'] == 'error', "Status should be error"


if __name__ == "__main__":
    try:
        test_printer_config_page()
        print("✓ test_printer_config_page passed")
        
        test_get_printer_profiles()
        print("✓ test_get_printer_profiles passed")
        
        test_create_printer_profile()
        print("✓ test_create_printer_profile passed")
        
        test_create_profile_without_name()
        print("✓ test_create_profile_without_name passed")
        
        test_update_printer_profile()
        print("✓ test_update_printer_profile passed")
        
        test_update_nonexistent_profile()
        print("✓ test_update_nonexistent_profile passed")
        
        test_delete_printer_profile()
        print("✓ test_delete_printer_profile passed")
        
        test_delete_default_profile()
        print("✓ test_delete_default_profile passed")
        
        test_delete_nonexistent_profile()
        print("✓ test_delete_nonexistent_profile passed")
        
        test_get_printer_presets()
        print("✓ test_get_printer_presets passed")
        
        test_generate_print_preview()
        print("✓ test_generate_print_preview passed")
        
        test_preview_without_data()
        print("✓ test_preview_without_data passed")
        
        print("\nAll printer tests passed!")
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        sys.exit(1)
