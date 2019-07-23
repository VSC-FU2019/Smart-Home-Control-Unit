import pyaudio
from python_speech_features import mfcc,delta
import numpy as np
import time
import sys

import keras
from keras.models import load_model
import tensorflow as tf 
#from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing.sequence import pad_sequences
#from threading import Thread
from queue import Queue

NUMB_CEP = 13
DELTA = 2
MFCC_LEN = 200

def get_feature(y, fs):
    y = y / np.max(abs((y)))
    mfcc_feat = mfcc(y, fs, numcep=NUMB_CEP)
    mfcc_feat = delta(mfcc_feat, DELTA)
                    
    return mfcc_feat
                              
def get_data(y, fs):
    input_data = []
    mfcc_feat = get_feature(y, fs)

    mfcc_feat = pad_sequences(mfcc_feat.T, MFCC_LEN, dtype=float, padding='post', truncating='post').T
    input_data = np.array([mfcc_feat])
    return input_data

def print_command(probabilities):
    arg_max = np.argmax(probabilities[0])
    if probabilities[0, arg_max] >= 0.75:
        if arg_max == 0:
            print("Background")
        elif arg_max == 1:
            print("Bat den")
        elif arg_max == 2:
            print("Tat den")
        elif arg_max == 3:
            print("Bat dieu hoa")
        elif arg_max == 4:
            print("Tat dieu hoa")
        elif arg_max == 5:
            print("Bat quat")
        elif arg_max == 6:
            print("Tat quat")
        elif arg_max == 7:
            print("Bat tivi")
        elif arg_max == 8:
            print("Tat tivi")
        elif arg_max == 9:
            print("Mo cua")
        elif arg_max == 10:
            print("Dong cua")
        elif arg_max == 11:
            print("Khoa cua")
        elif arg_max == 12:
            print("Mo cong")
        elif arg_max == 13:
            print("Dong cong")
        elif arg_max == 14:
            print("Khoa cong")
        elif arg_max == 15:
            print("Doremon")
        else:
            print("-")

config = tf.ConfigProto( ) 
sess = tf.Session(config=config) 
keras.backend.set_session(sess)
model= load_model('train.h5')
print('load model successfully')
q = Queue()

data = np.zeros(8000, dtype='int16')

def callback(in_data, frame_count, time_info, status):
    global data, q
    data0 = np.frombuffer(in_data, 'int16')
    data = np.append(data, data0)
    if len(data) > 16000:
        data = data[-16000:]
        q.put(data)
    return (data, pyaudio.paContinue)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=8000, input=True, frames_per_buffer=4000, stream_callback=callback)

stream.start_stream()
print('starting record')
try:
    while stream.is_active():
        start_time = time.time()
        x = get_data(q.get(), 8000)
        #print(data_8k.shape, x.shape)
        prob = model.predict(x)
        print(np.argmax(prob[0]))
        #print_command(prob)
        print("%s seconds" % (time.time() - start_time))
            
except (KeyboardInterrupt, SystemExit):
    stream.stop_stream()
    stream.close()

stream.stop_stream()
stream.close()
audio.terminate()






