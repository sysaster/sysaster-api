from flask import Flask, request

app = Flask(__name__)

@app.route("/detections/person", methods=['POST'])
def save_person_detection_data():
    if request.method == 'POST':
        return "person detection done"

