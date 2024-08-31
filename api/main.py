from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/api/hello', methods=['GET'])
def api_hello():
    return jsonify({"message": "Hello from Flask API"})

if __name__ == '__main__':
    app.run(debug=True)
