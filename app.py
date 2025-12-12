"""
Hello World API using Flask
A simple REST API that returns a hello world message.
"""
from flask import Flask, jsonify

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
            '/hello': 'Returns hello world message'
        }
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
