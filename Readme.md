# Voice Recognition

This is a full-stack project for voice recognition system.

Different types of technologies such as `DeepLearning` and `WebServers` are used here.

To have a good performance on different operating systems `docker` is used here.

# Dataset

The dataset for simple words which is called speech commands dataset 
can be downloaded from <a href="https://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html">here</a>.

# File By File Descriptions

## Prepare dataset

As for the neural network we need numerical data, so a conversion from audio files to something numerical is needed.
This is done in `prepare_dataset.py` file. This file makes a `json` file called `data.json` that has some informations about dataset 
like numberical data which is calculated by `librosa` or their label or all the categories.

## Model

In this file we have builing and training the model which is a convolutional neural netowork.

It first loads the data from the json file we mentioned earlier, then we split data to train, test, and validation sets using `sklearn`.

### Network

Here is the shape of neural network:

![image](./images/network1.png)

And here is datails:

![image](./images/network2.png)

*Made By Amirhossein Abaskohi*