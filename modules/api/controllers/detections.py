import os
from flask import Flask, request, jsonify, request
from api import app, mongo, fcm
import random
import utils
from enum import Enum
import sys
from bson.objectid import ObjectId
import numpy as np
import cv2
import base64

class ErrorCode(Enum):
    NO_TOPIC_FOUND=2,
    BAD_PARAMS=3

@app.route("/detections/<id>", methods=['GET'])
def detection_by_id(id):
    '''
    Receive a detection data and process it.
    '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.detections.find_one({'_id': ObjectId(id)})
        return jsonify(data), 200

@app.route("/detections", methods=['POST', 'GET'])
def detection():
    '''
    Receive a detection data and process it.
    '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.detections.find(query)
        return jsonify([d for d in data]), 200

    if request.method == 'POST':
        json_data = request.get_json(force=True)
        topic = json_data.get("topic", None)

        clipped_image = json_data.get("clipped_image", None)

        if clipped_image is not None:
            img_data = base64.b64decode(clipped_image)
            nparr = np.fromstring(img_data, dtype=np.uint8)

            bounding_box = json_data.get("bounding_box", None)
            
            if bounding_box is not None:
                w = bounding_box.get("w", None)
                h = bounding_box.get("h", None)
                c = bounding_box.get("c", None)
                if w is not None and h is not None and c is not None:
                    nparr = nparr.reshape(int(c) * int(h), int(w))
                    b = nparr[0:int(h),:]
                    g = nparr[int(h):2*int(h),:]
                    r = nparr[2*int(h):3*int(h),:]
                    img = cv2.merge((b, g, r))

                    _, buf = cv2.imencode('.jpg', img)
                    jpg_as_text = base64.b64encode(buf)
                    json_data['clipped_image'] = jpg_as_text.decode('utf-8')

        if topic is not None:
            topic_from_db = mongo.db.topics.find_one({'code':topic})
            if topic_from_db is not None:
                r = mongo.db.detections.insert_one({**json_data, 'topic':topic_from_db})
                if r is None:
                    return jsonify({'ok': False, 'msg': 'Insertion failed'}), 500
                # prepare and message
                message = {k:str(v) for k,v in json_data.items()}
                if 'clipped_image' in message:
                    del message['clipped_image']
                message["topic_name"] = topic_from_db["name"]
                message["id"] = str(r.inserted_id)
                fcm.send_message(message, topic)
                return jsonify({'ok': True, 'msg': 'Detection successfully received'}), 200
            else:
                return jsonify({'ok': False, 'msg': 'No topic with this code was found',
                    'code' : ErrorCode.NO_TOPIC_FOUND.value}), 400
        else:
            return jsonify({'ok': False, 'msg': 'Bad request parameters!', 'code': ErrorCode.BAD_PARAMS.value}), 400
