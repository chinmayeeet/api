import json
from pickle import TRUE
from flask import Flask, send_file
import functionpy as fu
from PIL import Image
import base64
from io import BytesIO
import requests
app = Flask(__name__)
import os, shutil
import mimetypes

@app.route('/')
def index():
   return "Hello World!"


@app.route('/perspective/<path:url>', methods=['GET'])
def api_index(url, asImage=True):
    # download the file from URL. Having unique name based on timestamp
    # run the file on cv and save the output
    from datetime import datetime
    dateTimeObj = datetime.now()
    file_name_for_base64_data = dateTimeObj.strftime("%d-%b-%Y--(%H-%M-%S)")
    
    #File naming process for directory form <file_name.jpg> data.
    #We are taken the last 8 characters from the url string.
    file_name_for_regular_data = url[-10:-4]

    dir_path = os.path.join(os.getcwdb().decode("utf-8"), "downloads") 
    base_url = "http://35.200.208.107/downloads/"

    result = {
        "result": False,
        "status": "unknown",
        "url": "",
    }
    
    # ----- SECTION 2 -----
    try:

        # Regular URL Form DATA
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers['content-type']
            extension = mimetypes.guess_extension(content_type)
            file_path = os.path.join(dir_path, file_name_for_regular_data + extension)
            with open(file_path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)  

            img = Image.open(file_path)
            out = fu.chpers(file_path, extension)
            img.save(out, file_path)

            url = base_url + file_name_for_regular_data + extension

            result["url"] = url
            result["result"] = True
            result["status"] = "success"
        else:
            result["url"] = ""
            result["result"] = False
            result["status"] = "URL not reachable"
        
    # ----- SECTION 3 -----    
        status = "Image has been succesfully sent to the server."
    except Exception as e:
        status = "Error! = " + str(e)

    return json.dumps(result, indent = 4) 

   

#@app.route('/', methods=['GET'])
#def index(url):
   # return "Hello World!"
    

app.run(host='0.0.0.0', port=80, debug=True)