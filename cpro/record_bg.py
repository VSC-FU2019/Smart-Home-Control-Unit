import pyaudio
from scipy.io import wavfile
import numpy as np

FORMAT = pyaudio.paInt16
CHANS = 1
RATE = 8000
CHUNK = 4000
SEC_REC = 2
NUMB_FILE = 500

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print('start ')
try:
    for f_index in range(2400, 10000, 1):
        samples = np.zeros(int(RATE * SEC_REC), dtype='int16')
        
        for i in range(4):
            samples[i * 4000: (i+1) * 4000] = np.frombuffer(stream.read(CHUNK), 'int16')
        
        wavfile.write('bg/' + str(f_index) + '.wav', RATE, samples)
            
        if f_index % 10 == 0:
            print('done %s' % f_index)
            
except (KeyboardInterrupt, SystemExit):
    print('keyboard, end')

stream.stop_stream()
stream.close()
audio.terminate()
    
