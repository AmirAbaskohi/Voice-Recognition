from numpy import np
import tensorflow.keras as keras

# This is a singleton class :
# Which means there is just one instance of it in program

MODEL_PATH = "model.h5"

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


    def preprocess(self, file_path):
        pass    


def word_spot_servie():

    if _WordSpotService._instance is None:
        
        _WordSpotService._instance = _WordSpotService()
        _WordSpotService.model = keras.models.load_model(MODEL_PATH)

    return _WordSpotService._instance