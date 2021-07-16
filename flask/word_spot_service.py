import numpy as np
import tensorflow.keras as keras
import librosa
import sys

# This is a singleton class :
# Which means there is just one instance of it in program

MODEL_PATH = "model.h5"
NUM_SAMPLES = 22050
SEPRATOR = ','

class _WordSpotService:
    
    model = None
    _mappings = [
        "six",
        "bird",
        "zero",
        "stop",
        "go",
        "happy",
        "nine",
        "sheila",
        "cat",
        "three",
        "on",
        "yes",
        "no",
        "two",
        "four",
        "off",
        "left",
        "bed",
        "tree",
        "right",
        "one",
        "five",
        "down",
        "house",
        "marvin",
        "dog",
        "eight",
        "seven",
        "up",
        "wow"
    ]
    _instance = None    \

    def predict(self, file_path):

        MFCCs = self.preprocess(file_path)

        MFCCs = MFCCs[np.newaxis, ..., np.newaxis]

        predictions = self.model.predict(MFCCs)
        predictions = np.argmax(predictions)
        predictions = self._mappings[predictions]

        return predictions


    def preprocess(self, file_path, n_mfccs= 13, n_fft=2048, hop_length=512):
        
        signal, sr = librosa.load(file_path)

        if len(signal) > NUM_SAMPLES:
            signal = signal[:NUM_SAMPLES]

        MFCCs = librosa.feature.mfcc(signal, n_mfcc=n_mfccs, n_fft=n_fft, hop_length=hop_length)

        return MFCCs.T


def word_spot_servie():

    if _WordSpotService._instance is None:
        
        _WordSpotService._instance = _WordSpotService()
        _WordSpotService.model = keras.models.load_model(MODEL_PATH)

    return _WordSpotService._instance

if __name__ == "__main__":

    wss = word_spot_servie()

    test_file_path = sys.argv[1]
    test_file = open(test_file_path, 'r')
    lines = test_file.readlines()

    for line in lines:
        if line[-1] == '\n':
            line = line[:-1]
        word, path = line.split(',')
        path = "tests/" + path
        print(f"Word: {word}, Predicted: {wss.predict(path)}")