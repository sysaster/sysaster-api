from flask import Flask, request
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/detections/person", methods=['POST'])
def save_person_detection_data():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        print(json_data["bounding_box"])
        img = cv2.imdecode(np.fromstring(json_data["clipped_image"], np.uint8), cv2.IMREAD_COLOR)
        print(img.rows, img.rows)
        cv2.imwrite("clipped.png", img);
        return "abc"

