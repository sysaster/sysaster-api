from flask import Flask, request
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route("/detections/person", methods=['POST'])
def save_person_detection_data():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        print(json_data["bounding_box"])
        nparr = np.fromstring(base64.b64decode(json_data["clipped_image"]), dtype=np.uint8)
        print(nparr)
        img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
        print(img)
        #cv2.imwrite("clipped.png", img);
        return "abc"

