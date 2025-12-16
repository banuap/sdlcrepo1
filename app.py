"""
Hello World API using Flask. This is a test.
A simple REST API that returns a hello world message.
"""
import os
import uuid
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# In-memory storage for printer profiles
printer_profiles = {
    'default': {
        'id': 'default',
        'name': 'Default Profile',
        'paper_size': 'Letter',
        'orientation': 'Portrait',
        'color_mode': 'Color',
        'quality': 'Standard',
        'duplex': False,
        'copies': 1,
        'is_favorite': True,
        'created_at': datetime.now().isoformat()
    }
}

# Job-specific presets
job_presets = {
    'draft_documents': {
        'name': 'Draft Documents',
        'paper_size': 'Letter',
        'orientation': 'Portrait',
        'color_mode': 'Grayscale',
        'quality': 'Draft',
        'duplex': True,
        'copies': 1
    },
    'photo_quality': {
        'name': 'Photo Quality',
        'paper_size': 'Photo 4x6',
        'orientation': 'Landscape',
        'color_mode': 'Color',
        'quality': 'High',
        'duplex': False,
        'copies': 1
    },
    'text_heavy': {
        'name': 'Text Heavy',
        'paper_size': 'Letter',
        'orientation': 'Portrait',
        'color_mode': 'Grayscale',
        'quality': 'Standard',
        'duplex': True,
        'copies': 1
    }
}


@app.route('/hello', methods=['GET'])
def hello_world():
    """
    Returns a hello world message.
    
    Returns:
        JSON response with a hello world message
    """
    return jsonify({
        'message': 'Hello World!',
        'status': 'success'
    })


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint that provides API information.
    
    Returns:
        JSON response with API information
    """
    return jsonify({
        'api': 'Hello World API',
        'version': '1.0',
        'endpoints': {
            '/': 'API information',
            '/hello': 'Returns hello world message',
            '/login': 'Login with username and password (POST)',
            '/welcome': 'Welcome page (HTML)',
            '/printer': 'Printer configuration UI (HTML)',
            '/printer/profiles': 'Printer profiles API',
            '/printer/presets': 'Job-specific presets API'
        }
    })


@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint that validates username and password.
    
    Expects JSON body with:
        username (str): The username
        password (str): The password
    
    Returns:
        JSON response with login status
    """
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'status': 'error',
            'message': 'Username and password are required'
        }), 400
    
    # Simple validation (in production, this should check against a database)
    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'username': username
    }), 200


@app.route('/welcome', methods=['GET'])
def welcome():
    """
    Welcome page that provides a friendly introduction to the API.
    
    Returns:
        HTML page with welcome message and API information
    """
    return render_template('welcome.html')


@app.route('/printer', methods=['GET'])
def printer_config():
    """
    Printer configuration UI page.
    
    Returns:
        HTML page with printer configuration interface
    """
    return render_template('printer_config.html')


@app.route('/printer/profiles', methods=['GET'])
def get_printer_profiles():
    """
    Get all printer profiles.
    
    Returns:
        JSON response with list of printer profiles
    """
    profiles_list = list(printer_profiles.values())
    return jsonify({
        'status': 'success',
        'profiles': profiles_list
    }), 200


@app.route('/printer/profiles', methods=['POST'])
def create_printer_profile():
    """
    Create a new printer profile.
    
    Expects JSON body with:
        name (str): Profile name
        paper_size (str): Paper size
        orientation (str): Page orientation
        color_mode (str): Color mode
        quality (str): Print quality
        duplex (bool): Enable duplex printing
        copies (int): Number of copies
        is_favorite (bool): Mark as favorite
    
    Returns:
        JSON response with created profile
    """
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    if not data.get('name'):
        return jsonify({
            'status': 'error',
            'message': 'Profile name is required'
        }), 400
    
    profile_id = str(uuid.uuid4())
    profile = {
        'id': profile_id,
        'name': data.get('name'),
        'paper_size': data.get('paper_size', 'Letter'),
        'orientation': data.get('orientation', 'Portrait'),
        'color_mode': data.get('color_mode', 'Color'),
        'quality': data.get('quality', 'Standard'),
        'duplex': data.get('duplex', False),
        'copies': data.get('copies', 1),
        'is_favorite': data.get('is_favorite', False),
        'created_at': datetime.now().isoformat()
    }
    
    printer_profiles[profile_id] = profile
    
    return jsonify({
        'status': 'success',
        'message': 'Profile created successfully',
        'profile': profile
    }), 201


@app.route('/printer/profiles/<profile_id>', methods=['PUT'])
def update_printer_profile(profile_id):
    """
    Update an existing printer profile.
    
    Args:
        profile_id (str): The profile ID
    
    Returns:
        JSON response with updated profile
    """
    if profile_id not in printer_profiles:
        return jsonify({
            'status': 'error',
            'message': 'Profile not found'
        }), 404
    
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    profile = printer_profiles[profile_id]
    
    # Update only provided fields
    if 'name' in data:
        profile['name'] = data['name']
    if 'paper_size' in data:
        profile['paper_size'] = data['paper_size']
    if 'orientation' in data:
        profile['orientation'] = data['orientation']
    if 'color_mode' in data:
        profile['color_mode'] = data['color_mode']
    if 'quality' in data:
        profile['quality'] = data['quality']
    if 'duplex' in data:
        profile['duplex'] = data['duplex']
    if 'copies' in data:
        profile['copies'] = data['copies']
    if 'is_favorite' in data:
        profile['is_favorite'] = data['is_favorite']
    
    profile['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'status': 'success',
        'message': 'Profile updated successfully',
        'profile': profile
    }), 200


@app.route('/printer/profiles/<profile_id>', methods=['DELETE'])
def delete_printer_profile(profile_id):
    """
    Delete a printer profile.
    
    Args:
        profile_id (str): The profile ID
    
    Returns:
        JSON response with deletion status
    """
    if profile_id not in printer_profiles:
        return jsonify({
            'status': 'error',
            'message': 'Profile not found'
        }), 404
    
    if profile_id == 'default':
        return jsonify({
            'status': 'error',
            'message': 'Cannot delete default profile'
        }), 400
    
    del printer_profiles[profile_id]
    
    return jsonify({
        'status': 'success',
        'message': 'Profile deleted successfully'
    }), 200


@app.route('/printer/presets', methods=['GET'])
def get_printer_presets():
    """
    Get job-specific presets.
    
    Returns:
        JSON response with available presets
    """
    return jsonify({
        'status': 'success',
        'presets': job_presets
    }), 200


@app.route('/printer/preview', methods=['POST'])
def generate_print_preview():
    """
    Generate a print preview based on provided settings.
    
    Expects JSON body with printer settings.
    
    Returns:
        JSON response with preview information
    """
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    preview = {
        'status': 'success',
        'preview': {
            'paper_size': data.get('paper_size', 'Letter'),
            'orientation': data.get('orientation', 'Portrait'),
            'color_mode': data.get('color_mode', 'Color'),
            'quality': data.get('quality', 'Standard'),
            'duplex': data.get('duplex', False),
            'copies': data.get('copies', 1),
            'estimated_pages': 1,
            'preview_text': 'This is a preview of how your document will be printed with the selected settings.'
        }
    }
    
    return jsonify(preview), 200


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
