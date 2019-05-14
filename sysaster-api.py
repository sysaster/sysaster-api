from flask import Flask, request

app = Flask(__name__)

@app.route("/detections/person", methods=['POST'])
def save_person_detection_data():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        print(len(json_data["clipped_image"]), json_data["clipped_image"])
        return "abc"

