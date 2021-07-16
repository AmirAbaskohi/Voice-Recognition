import uuid
import os
from flask import Flask, request, json
from word_spot_service import word_spot_servie

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    
    audio_file = request.files["file"]
    file_name = str(uuid.uuid4())
    audio_file.save(file_name)

    wss = word_spot_servie()
    predicted = wss.predict(file_name)

    os.remove(file_name)

    data = {"word": predicted}
    return json.jsonify(data)

if __name__ == "__main__":
    app.run(debug=False)