import pyaudio
import wave
import librosa
import numpy as np
from scipy.io import wavfile

form_1 = pyaudio.paInt16
chans = 1
fs = 8000
chunk = 2000
record_secs = 10
dev_index = 1
out_file = 'record test xa.wav'

audio = pyaudio.PyAudio()
stream = audio.open(format=form_1, rate=8000, channels=1, input=True, frames_per_buffer=2000)
print('recording')

frames = []

for ii in range(0, int(8000 / 2000) * record_secs):
	print(ii)
	data = stream.read(chunk)
	frames.append(data)
	
print('finish recording')
stream.stop_stream()
stream.close()
audio.terminate()

wf = wave.open(out_file, 'wb')
wf.setnchannels(chans)
wf.setsampwidth(audio.get_sample_size(form_1))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
print('done')

