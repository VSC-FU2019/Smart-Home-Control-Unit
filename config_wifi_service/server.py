from flask import Flask, render_template,request
from wifi import Cell
import os
import config
app = Flask(__name__)


def get_ssids():
    try:
       cells= Cell.all('wlan0')
    except:
       cells= []
    list_ssid = []
    for c in cells:
        list_ssid.append(c.ssid)
    return list_ssid

@app.route('/update', methods=['POST'])
def connect():
    if request.method=='POST':
       os.system("../update.sh")
       return render_template('index.html', message_update="Updating firmware, please wait to reset")

@app.route('/', methods=['POST','GET'])
def connect2():
    if request.method=='POST':
       list_ssid = get_ssids()
       result = request.form
       ssid = None
       psk = None
       for key, value in result.items():
          if key == "ssid":
             ssid= value
          if key =="pwd":
             psk = value
       ip= config.connect(ssid, psk)
       print(ip)
       if ip=='error':
          return render_template('index.html', ssids= list_ssid, message="connect fail")
       return render_template('index.html', ssids=list_ssid, message="connect successful with ip = "+ ip)
    if request.method=='GET':
       list_ssid = get_ssids()
       return render_template('index.html', ssids=list_ssid)


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
