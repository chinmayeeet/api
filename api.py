import json
from flask import Flask, send_file
import code as code
app = Flask(__name__)


@app.route('/api/<url>', methods=['GET'])
def api_index(url):
    # download the file from URL. Having unique name based on timestamp
    # run the file on cv and save the output
    out = code.chpers(url)
    return(out)

@app.route('/api/<url>', methods=['GET'])
def index(url):
    out = code.chpers(url)
    return(out)

app.run(host='0.0.0.0', port=80, debug=True)