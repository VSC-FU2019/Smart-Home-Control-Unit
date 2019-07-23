import subprocess 
import time
import os
import netifaces as ni
def connect(ssid,pwd):

    ssid=ssid
    psk = pwd
    key_mgmt='WPA-PSK'
    os.system('sudo wpa_cli remove_network all')
    os.system('sudo wpa_cli add_network')
    p = os.system('sudo wpa_cli set_network 0 ssid \'\"'+ ssid +'\"\'')
    print(p)
    if(p=='OK'):
      print('run')
    os.system('sudo wpa_cli set_network 0 psk \'\"'+psk+'\"\'')
    os.system('sudo wpa_cli set_network 0 key_mgmt "WPA-PSK"')
    os.system('sudo wpa_cli enable_network 0')
    os.system('sudo wpa_cli save_config')
    os.system('sudo wpa_cli -i wlan0 reconfigure')
    ni.ifaddresses('wlan0')
    time.sleep(15)
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    print(ip)
    return ip
