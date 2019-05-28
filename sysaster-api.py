from flask import Flask, request
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route("/detections/person", methods=['POST'])
def save_person_detection_data():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        img_data = base64.b64decode(json_data["clipped_image"])
        nparr = np.fromstring(img_data, dtype=np.uint8)
        w = json_data["bounding_box"]["w"]
        h = json_data["bounding_box"]["h"]
        nparr = nparr.reshape(int(h), int(w))
        cv2.imwrite("clipped.png", nparr);
        return "abc"

