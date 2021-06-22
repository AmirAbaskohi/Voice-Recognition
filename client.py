import requests
import sys
from werkzeug.wrappers import response

URL = "http://127.0.0.1:5000/predict"

if __name__ == "__main__":

    audio_name = sys.argv[1]
    audio_path = "tests/" + audio_name

    try:
        audio_file = open(audio_path, "rb")
        values = {"file": (audio_path, audio_file, "audio/wav")}

        response = requests.post(URL, files=values)
        data = response.json()

        print(f"Predicted word is : {data['word']}")
    
    except:
        print("Something went wrong")
        print("Make sure your file exist in tests folder")
