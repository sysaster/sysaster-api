from flask import Flask, request
import cv2
import numpy as np
import base64
import random

app = Flask(__name__)

@app.route("/detections/person", methods=['POST'])
def save_person_detection_data():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        img_data = base64.b64decode(json_data["clipped_image"])
        nparr = np.fromstring(img_data, dtype=np.uint8)
        w = json_data["bounding_box"]["w"]
        h = json_data["bounding_box"]["h"]
        c = json_data["bounding_box"]["c"]
        nparr = nparr.reshape(int(c) * int(h), int(w))
        b = nparr[0:int(h),:]
        g = nparr[int(h):2*int(h),:]
        r = nparr[2*int(h):3*int(h),:]
        img = cv2.merge((b, g, r))
        img_rand_id = random.random()*100
        cv2.imwrite("clipped_"+str(img_rand_id)+".png", img);
        return "abc"

