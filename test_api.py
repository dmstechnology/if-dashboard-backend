from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def hello_world():
    data = {
        'message': 'Hello, World!'
    }
    return jsonify(data)  # Return JSON response

if __name__ == '__main__':
    app.run(debug=True)
