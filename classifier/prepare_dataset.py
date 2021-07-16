import librosa
import os
import json


DATASET_PATH = "Dataset"
JSON_PATH = "data.json"
SAMPLES_TO_CONSIDER = 22050

def prepare_dataset(dataset_path, json_path, n_mfcc=13, hop_length=512, n_fft=2048):

    data = {
        "mappings": [],
        "labels": [],
        "MFCCs": [],
        "files": []
    }

    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):

        if dirpath is not dataset_path:

            category = dirpath.split("/")[-1]

            data["mappings"].append(category)
            print(f"Processing {category}")

            for file_name in filenames:
                
                file_path = os.path.join(dirpath, file_name)
                signal, sr = librosa.load(file_path)

                if len(signal) >= SAMPLES_TO_CONSIDER:
                    
                    signal = signal[:SAMPLES_TO_CONSIDER]
                    MFCCs = librosa.feature.mfcc(signal, n_mfcc=n_mfcc, hop_length=hop_length, n_fft=n_fft)
                    
                    data["labels"].append(i-1)
                    data["MFCCs"].append(MFCCs.T.tolist())
                    data["files"].append(file_path)
                    print(f"{file_path} : {i-1}")

    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    prepare_dataset(DATASET_PATH, JSON_PATH)
