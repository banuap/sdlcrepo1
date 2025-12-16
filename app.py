"""
Hello World API using Flask. This is a test.
A simple REST API that returns a hello world message.
"""
import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


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
            '/welcome': 'Welcome page (HTML)'
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


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
