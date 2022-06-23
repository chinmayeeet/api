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
    
    # ----- SECTION 2 -----
    try:
        # Base64 DATA
        if "data:image/jpeg;base64," in url:
            base_string = url.replace("data:image/jpeg;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

            file_name = file_name_for_base64_data + ".jpg"
            return(file_name)
            #out = fu.chpers(file_name)
            #img.save(out, "jpeg")

        # Base64 DATA
        elif "data:image/png;base64," in url:
            base_string = url.replace("data:image/png;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

            file_name = file_name_for_base64_data + ".png"
            out = fu.chpers(file_name)
            img.save(out, "png")

        # Regular URL Form DATA
        else:
            response = requests.get(url)
            if response.status_code == 200:
                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                file_path = os.path.join(dir_path, file_name_for_regular_data, extension)
                with open(file_path, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)  

                img = Image.open(file_path)
                out = fu.chpers(file_path)
                img.save(out, file_path)
        
    # ----- SECTION 3 -----    
        status = "Image has been succesfully sent to the server."
    except Exception as e:
        status = "Error! = " + str(e)

    return status

   

#@app.route('/', methods=['GET'])
#def index(url):
   # return "Hello World!"
    

app.run(host='0.0.0.0', port=80, debug=True)