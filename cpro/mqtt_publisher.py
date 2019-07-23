import paho.mqtt.publish as publisher
import Constant
import time
from gpiozero import LED
import os

class MqttPublisher():
    def __init__(self, led):
        self.led = led
        self.command_series = []
        self.said_trigger_word = False
        self.trigger_word_time_life = 0
        self.command_dictionary = {
            1: {'topic': 'light', 'action': 'on'},
            2: {'topic': 'light', 'action': 'off'},
            3: {'topic': 'airconditioner', 'action': 'on'},
            4: {'topic': 'airconditioner', 'action': 'off'},
            5: {'topic': 'fan', 'action': 'on'},
            6: {'topic': 'fan', 'action': 'off'},
            7: {'topic': 'tivi', 'action': 'on'},
            8: {'topic': 'tivi', 'action': 'off'},
            9: {'topic': 'door', 'action': 'open'},
            10: {'topic': 'door', 'action': 'close'},
            11: {'topic': 'door', 'action': 'lock'},
            12: {'topic': 'gate', 'action': 'open'},
            13: {'topic': 'gate', 'action': 'close'},
            14: {'topic': 'gate', 'action': 'lock'}
        }
        
    def handle(self, command_index, command_prob):
        """
        Xu ly voi input la command index (0 - 15) va xac suat predict (0.0 - 1.0)
        Neu co 3 command giong nhau lien tiep voi xac suat deu tren 75% thi publish len MQTT broker
        """
        if self.said_trigger_word:
            ## moi lan predict tuong duong voi 0.5s
            self.trigger_word_time_life += 0.5
            
        if self.trigger_word_time_life == 10:
            ## thoi gian toi da tu luc noi trigger word den khi noi command la 5s
            #print("end")
            self.led.off()
            self.said_trigger_word = False
            self.trigger_word_time_life = 0
        
        ## logic quyet dinh command hop le
        if command_prob >= Constant.MIN_COMMAND_PROB:
            if len(self.command_series) > 0 and command_index != self.command_series[-1]:
                del self.command_series[:]

            self.command_series.append(command_index)
            
            if len(self.command_series) == 3:
                if command_index == Constant.TRIGGER_WORD_INDEX:
                    #print('Doraemon')
                #    os.system('aplay -D loa /home/pi/cpro/xin_chao.wav')
                    self.led.on()
                    self.said_trigger_word = True
                    self.trigger_word_time_life = 0
                else:
                    if self.said_trigger_word:
                        if command_index != 0:
                            print(command_index)
                            publisher.single(self.command_dictionary[command_index]['topic'], self.command_dictionary[command_index]['action'], hostname=Constant.MQTT_BROKER_IP)
    
                            ## reset
                            self.said_trigger_word = False
                            self.trigger_word_time_life = 0
                            
                            ## nhap nhay led
                            self.led.off()
                            time.sleep(0.2)
                            self.led.on()
                            time.sleep(0.2)
                            self.led.off()
                            time.sleep(0.2)
                            self.led.on()
                            time.sleep(0.2)
                            self.led.off()
                del self.command_series[:]
        else:
            ## reset command series
            del self.command_series[:]
