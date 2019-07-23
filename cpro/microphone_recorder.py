import pyaudio
from python_speech_features import mfcc,delta
import Constant
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import time
from scipy.signal import butter, lfilter
class MicrophoneRecorder():
    def __init__(self, queue):
        self.queue = queue
        self.data = np.zeros(Constant.PREDICT_SAMPLES, dtype='int16')
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=Constant.CHANNEL_NUMB, rate=Constant.RATE,
                                 input=True, frames_per_buffer=Constant.REC_CHUNK, stream_callback=self.audio_callback)
    
    
    def start_record(self):
        self.stream.start_stream()
        print('---------------- Start recording -----------------')
        
    def close_record(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        #start_time = time.time()
        rec_data = np.frombuffer(in_data, 'int16')
        self.data = np.append(self.data, rec_data)
        
        if len(self.data) > Constant.PREDICT_SAMPLES:
            self.data = self.data[-Constant.PREDICT_SAMPLES:]
            mfcc_feat = self.feature_extract(self.data)
            self.queue.put(mfcc_feat)
        return (None, pyaudio.paContinue)
    
    def butter_bandpass(self,lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a


    def butter_bandpass_filter(self,data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def feature_extract(self, data):
        #data = self.butter_bandpass_filter(data,300,3400,Constant.RATE)
        normalized_data = data / np.max(abs(data))
        mfcc_feat = mfcc(normalized_data, Constant.RATE)
        mfcc_feat = delta(mfcc_feat, Constant.DELTA)
        return np.array([pad_sequences(mfcc_feat.T, Constant.MFCC_LEN, dtype=float, padding='post', truncating='post').T])

        
