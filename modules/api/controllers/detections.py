import os
from flask import Flask, request, jsonify, request
from api import app, mongo
import random
import utils

@app.route("/detections", methods=['POST'])
def receive_detection_data():
    '''
    Receive a detection data and process it.
    '''
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        topic = json_data["topic"]
        fmc.send_message(json_data, topic)
        #img_data = json_data["clipped_image"]
        #w = json_data["bounding_box"]["w"]
        #h = json_data["bounding_box"]["h"]
        #c = json_data["bounding_box"]["c"]
        #img = decode_base64_img(img_data, w, h, c)
        #img_rand_id = random.random()*100
        #cv2.imwrite("clipped_"+str(img_rand_id)+".png", img);

