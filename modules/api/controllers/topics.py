import os
from flask import request, jsonify
from api import app, mongo, fcm
from enum import Enum

class ErrorCode(Enum):
    DUPLICATE_CODE=1,
    NO_TOPIC_FOUND=2,
    BAD_PARAMS=3,

@app.route("/topics", methods=['POST', 'GET'])
def topic():
    '''
    Create a topic in the database, that will be
    available to be used in the notifications
    service.
    '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.topics.find(query)
        return jsonify([d for d in data]), 200

    data = request.get_json(force=True)

    if request.method == 'POST':
        code = data.get("code", None)
        date = data.get("date", None)
        name = data.get("name", None)
        lat = data.get("lat", None)
        lon = data.get("lon", None)

        # check for unique code
        if  code is not None:
            topic_from_db = mongo.db.topics.find_one({'code':code})
            if topic_from_db is not None:
                return jsonify({'ok': False, 'msg': 'Duplicated code', 'code': ErrorCode.DUPLICATE_CODE.value}), 400

        if  code is not None and \
            date is not None and \
            name is not None and \
            lat is not None and \
            lon is not None:
            mongo.db.topics.insert_one(data)
            return jsonify({'ok': True, 'msg': 'Topic created successfully'}), 200
        else:
            return jsonify({'ok': False, 'msg': 'Bad request parameters!', 'code': ErrorCode.BAD_PARAMS.value}), 400

@app.route("/topics/subscribe", methods=['POST'])
def subscribe_to_topic():
    '''
    Subscribe an app to a topic.
    '''
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        topic = json_data.get("topic", None)
        token = json_data.get("token", None)

        if  topic is None or \
            token is None:
            return jsonify({'ok': False, 'msg': 'Bad request parameters!', 'code': ErrorCode.BAD_PARAMS.value}), 400

        topic_from_db = mongo.db.topics.find_one({'code':topic})

        if topic_from_db is not None:
            fcm.subscribe_to_topic(token, topic)
            return jsonify({'ok': True, 'msg': 'Successfully subscribed'}), 200
        else:
            return jsonify({'ok': False, 'msg': 'No topic with this code was found',
                'code':ErrorCode.NO_TOPIC_FOUND.value}), 400

@app.route("/topics/unsubscribe", methods=['POST'])
def unsubscribe_to_topic():
    '''
    Unsubscribe an app from a topic.
    '''
    if request.method == 'POST':
        json_data = request.get_json(force=True)

        topic = json_data.get("topic", None)
        token = json_data.get("token", None)

        if  topic is None or \
            token is None:
            return jsonify({'ok': False, 'msg': 'Bad request parameters!', 'code': ErrorCode.BAD_PARAMS.value}), 400

        topic_from_db = mongo.db.topics.find_one({'code':topic})

        if topic_from_db is not None:
            fcm.unsubscribe_from_topic(token, topic)
            return jsonify({'ok': True, 'msg': 'Successfully unsubscribed'}), 200
        else:
            return jsonify({'ok': False, 'msg': 'No topic with this code was found',
                    'code' : ErrorCode.NO_TOPIC_FOUND.value}), 400
