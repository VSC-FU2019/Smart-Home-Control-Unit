import pyaudio
from gpiozero import LED
import time
import os
from queue import Queue
from queue import Empty as QueueEmpty
import threading
## class coding by myself
from microphone_recorder import MicrophoneRecorder
from mqtt_publisher import MqttPublisher
from command_prediction import CommandPrediction
start_model = 1
led = LED(17)

def load():
    global led
    global start_model
    while start_model:
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)


if __name__ == '__main__':
    ## configure ALSA
    os.system('cp ~/asoundrc.txt ~/.asoundrc')
    thread_load = threading.Thread(target=load)
    thread_load.start()
    model = CommandPrediction()
    mqtt_publisher = MqttPublisher(led)
    queue = Queue()
    recorder = MicrophoneRecorder(queue)
    start_model = 0
    #mqtt_client.connect("192.168.1.77", port=1883, keepalive=60) #dien IP cua Pi, vd: 192.168.1.77
    recorder.start_record()
    
    try:
        while recorder.stream.is_active():
            try:
                #start_time = time.time()
                feature_tensor = queue.get()
                
                command_index, command_prob = model.predict(feature_tensor)
                
                mqtt_publisher.handle(command_index, command_prob)
                #print('%s seconds' % (time.time() - start_time))
            except QueueEmpty:
                continue
                
    except (KeyboardInterrupt, SystemExit):
        print('End program')
        start_model = 0
    led.off()
    recorder.close_record()
    
