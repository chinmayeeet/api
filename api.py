import json
from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/api/v1.0/img/<int:task_id>', methods=['POST'])
def index():
    return jsonify({'name': 'alice',
                       'email': 'alice@outlook.com'})
app.run()