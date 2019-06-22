import os
from flask import Flask, request, jsonify, request
from api import app, mongo, fcm
import random
import utils
from enum import Enum

class ErrorCode(Enum):
    NO_TOPIC_FOUND=2,
    BAD_PARAMS=3

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

        if topic is not None:
            topic_from_db = mongo.db.topics.find_one({'code':topic})
            if topic_from_db is not None:
                r = mongo.db.detections.insert_one({**json_data, 'topic':topic_from_db})
                if r is None:
                    return jsonify({'ok': False, 'msg': 'Insertion failed'}), 500
                # prepare and message
                message = {k:str(v) for k,v in json_data.items()}
                message["topic_name"] = topic_from_db["name"]
                fcm.send_message(message, topic)
                return jsonify({'ok': True, 'msg': 'Detection successfully received'}), 200
            else:
                return jsonify({'ok': False, 'msg': 'No topic with this code was found',
                    'code' : ErrorCode.NO_TOPIC_FOUND.value}), 400
        else:
            return jsonify({'ok': False, 'msg': 'Bad request parameters!', 'code': ErrorCode.BAD_PARAMS.value}), 400
