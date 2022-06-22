import json
from flask import Flask, send_file
import code as code
app = Flask(__name__)
@app.route('/api/v1.0/<filename>', methods=['GET'])
def index(filename):
    out = code.chpers(filename)
    return(out)
app.run()