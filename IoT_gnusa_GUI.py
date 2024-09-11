import tkinter
from tkinter import *
import datetime
from datetime import date
import urllib.request
import time

import requests
import re
import numpy as np
import uuid
import urllib.request
import datetime
from datetime import date
from datetime import datetime
import os, glob

#import json
#from datetime import datetime
global device_id, resend_time, jam, last_send, file_del_days
device_id = ""#"DENCITY-Playup.2409.00001"

jam = 0
last_send = 0
# hari delete file kismet
file_del_days = 10
# periode cek data dan kirim ke server
resend_time = 10

KISMET_USER = "KISMET_USER"
KISMET_PASSWORD = "KISMET_PASSWORD"

username = os.environ.get('SUDO_USER', os.environ.get('USERNAME'))

path_kismet_data = os.path.expanduser(f'~{username}')
print(path_kismet_data)

# URL Kismet API

KISMET_URL = f"http://{KISMET_USER}:{KISMET_PASSWORD}@localhost:2501"
api_key = "D80B96E4D7E4614D9926A0BAD9C9B6F2"         # Ganti dengan API key Anda

# Header untuk otorisasi
headers1 = {
    "Authorization": f"Basic {api_key}"
}
headers_data = {"Content-Type": "application/json; charset=utf-8",'XA': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdfaWQiOiJERU5DSVRZIiwiaWF0IjoxNzI1NTI3NzY0fQ.1X0pGlp5MEB72489yGXN2re9jTF9B6HyJuxE054Bcsk'}
#headers_data = {"Content-Type": "application/json; charset=utf-8",'uspw': '{"user":"admin@playup.com","pass":"playup123"}'}
headers_regis = {"Content-Type": "application/json; charset=utf-8"}
# Endpoint untuk mendapatkan perangkat yang terdeteksi
#DEVICES_ENDPOINT = "/devices/views/physdevices.json"
DEVICES_ENDPOINT = "/devices/last-time/0/devices.json"
url_data = 'https://adm-iot.gnusa.id/service/device_transmit'
url_regis = 'https://adm-iot.gnusa.id/service/reg_mac_address'
      #'https://adm-iot.gnusa.id/service/device_transmit'
# Header untuk otorisasi
headers1 = {
    "Authorization": f"Basic {api_key}"
}




class App:
    def __init__(self, window, window_title):


        self.window = window
        self.window.title(window_title)
        window_height = 400
        window_width = 400

        screen_width = self.window .winfo_screenwidth()
        screen_height = self.window .winfo_screenheight()
        
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))


        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.window.rowconfigure(0, minsize=100, weight=1)
        self.window.columnconfigure(1, minsize=200, weight=1)
        
        fr_button = Frame(self.window)
        fr_graph = Frame(self.window)
        fr_result = Frame(self.window)
        
        self.btn_quit = Button(fr_button, text="Quit", command=self.window.destroy)
        self.btn_quit.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.btn_quit.config(width=10, height=5)
        
        self.lbl_obj = Label(fr_button, text="Summary:", font=('Times 14'))
        self.lbl_obj.grid(row=15, column=0, padx=10, pady=5, sticky="w")

        self.lbl_mac = Label(fr_button, text="MAC Address", font=('Times 14'))
        self.lbl_mac.grid(row=16, column=0, padx=10, pady=5, sticky="w")
        self.lbl_macval = Label(fr_button, text=": 0 ", font=('Times 14'))
        self.lbl_macval.grid(row=16, column=1, padx=5, pady=5, sticky="w")

        self.lbl_mag_max = Label(fr_button, text="Device ID", font=('Times 14'))
        self.lbl_mag_max.grid(row=17, column=0, padx=10, pady=5, sticky="w")
        self.lbl_batu = Label(fr_button, text=": 0 ", font=('Times 14'))
        self.lbl_batu.grid(row=17, column=1, padx=5, pady=5, sticky="w")

        self.lbl_phase_min = Label(fr_button, text="Status", font=('Times 14'))
        self.lbl_phase_min.grid(row=18, column=0, padx=10, pady=5, sticky="w")
        self.lbl_cy = Label(fr_button, text=": 0", font=('Times 14'))
        self.lbl_cy.grid(row=18, column=1, padx=5, pady=5, sticky="w")

        self.lbl_phase_max = Label(fr_button, text="Last sent", font=('Times 14'))
        self.lbl_phase_max.grid(row=19, column=0, padx=10, pady=5, sticky="w")
        self.lbl_val = Label(fr_button, text=": None", font=('Times 14'))
        self.lbl_val.grid(row=19, column=1, padx=5, pady=5, sticky="w")

        self.lbl_con = Label(fr_button, text="Connection ", font=('Times 14'))
        self.lbl_con.grid(row=20, column=0, padx=10, pady=5, sticky="w")
        self.lbl_conval = Label(fr_button, text=": None", font=('Times 14'))
        self.lbl_conval.grid(row=20, column=1, padx=5, pady=5, sticky="w")
        
        self.lbl_con11 = Label(fr_button, text="Current Time ", font=('Times 14'))
        self.lbl_con11.grid(row=21, column=0, padx=10, pady=5, sticky="w")
        self.lbl_conval1 = Label(fr_button, text=": None", font=('Times 14'))
        self.lbl_conval1.grid(row=21, column=1, padx=5, pady=5, sticky="w")

        fr_button.grid(row=0, column=0, sticky="ns")
        fr_graph.grid(row=0, column=1, sticky="nsew")
        fr_result.grid(row=0, column=2, sticky="nsew")

        
        self.window.after(2000, self.timer)

        self.window.mainloop()
        
    def get_mac_address(self):
        mac_address = uuid.getnode()
        mac_address_id = (':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])).upper()
        print("mac")
        print(mac_address_id)
        #mac_address_id = "7C:83:34:BB:74:D1"
        
        return mac_address_id
    
    def date_filename (self):
        current_time = datetime.datetime.now()        
        str_tgl = str(current_time.year) + "_" + str(current_time.month) + "_" + str(current_time.day)
        return str(str_tgl)
    
    def get_date_time_file (self):
        current_time = datetime.datetime.now()
        #print(current_time)
        tgl = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day)
        #print(tgl)
        jam = str(current_time.hour) + ":" + str(current_time.minute) + ":" + str(current_time.second)
        #print(jam)
        str_date_time = str(current_time.year) + "/" + str(current_time.month) + "/" + str(current_time.day) +" " + str(current_time.hour) + ":" + str(current_time.minute) + ":" + str(current_time.second)
        
        #print(str_date_time)
        return str_date_time
    
    def delete_old_file(self):
        current_time = str(datetime.now().strftime("%Y%m%d"))
        
        os.chdir(path_kismet_data)
        #for fileN in os.listdir(path_kismet_data):
        for fileN in glob.glob("*.kismet"):
            
            x = fileN.split("-")
            today = datetime.now().strftime("%Y-%m-%d")
            #year = today.year
            date_create = date(int(x[1][0:4]),int(x[1][4:6]),int(x[1][6:9]))            
            get_diff_days = (date.today() - date_create).days
            
            # file_del_days
            if get_diff_days > file_del_days:
                isExistdelKISMET = os.path.exists(path_kismet_data + "/" + fileN)
                if isExistdelKISMET:
                    os.remove(path_kismet_data + "/" + fileN)
    
    def get_device_id (self):
        global device_id
        data_device ={
        "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdfaWQiOiJERU5DSVRZIiwiaWF0IjoxNzI1NTI3NzY0fQ.1X0pGlp5MEB72489yGXN2re9jTF9B6HyJuxE054Bcsk",
        "mac_address":self.get_mac_address(),
        "device_type":"Mini PC"}
        
        try:
            response = requests.post(url_regis, headers=headers_regis, json=data_device)
            print("Status Code", response.status_code)
            res_json = response.json()
            print("JSON Response ", res_json)
            device_id = res_json["data"]["device_id"]
            #print(type(response.json()))
            #print(res_json["data"]["device_id"])
            #print(response)
            
            #response = requests.post(PHP_URL, data=payload)
            #print(response)
            #response.raise_for_status()
            print(f"Data get device id successfully")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to get device id")
            return False
    
    def estimate_distance(self, power_received, params=None):
        """This function returns an estimated distance range
           given a single radio signal strength (RSS) reading
           (received power measurement) in dBm.


        Parameters:
            power_received (float): RSS reading in dBm
            params (4-tuple float): (d_ref, power_ref, path_loss_exp, stdev_power)
                d_ref is the reference distance in m
                power_ref is the received power at the reference distance
                path_loss_exp is the path loss exponent
                stdev_power is standard deviation of received Power in dB

        Returns:
            (d_est, d_min, d_max): a 3-tuple of float values containing
                the estimated distance, as well as the minimum and maximum
                distance estimates corresponding to the uncertainty in RSS,
                respectively, in meters rounded to two decimal points
        """

        if params is None:
            params = (1.0, -55.0, 2.0, 2.5)
              # the above values are arbitrarily chosen "default values"
              # should be changed based on measurements

        d_ref = params[0] # reference distance
        power_ref = params[1] # mean received power at reference distance
        path_loss_exp = params[2] # path loss exponent
        stdev_power = params[3] # standard deviation of received power

        uncertainty = 2*stdev_power # uncertainty in RSS corresponding to 95.45% confidence

        d_est = d_ref*(10**(-(power_received - power_ref)/(10*path_loss_exp)))
        d_min = d_ref*(10**(-(power_received - power_ref + uncertainty)/(10*path_loss_exp)))
        d_max = d_ref*(10**(-(power_received - power_ref - uncertainty)/(10*path_loss_exp)))

        return (np.round(d_est,2), np.round(d_min,2), np.round(d_max,2))

    def get_devices(self):
        try:
            response = requests.get(f"{KISMET_URL}{DEVICES_ENDPOINT}", headers=headers1)
            
            if response.status_code == 200:
                return response.json()  # Mengembalikan data dalam format JSON
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
            
    def submit_device_data(self, device):
        global last_send, sig, distance, min_dist, max_dist, last_noise, min_noise, max_noise
        sig = 0
        distance = 0
        min_dist = 0
        max_dist = 0
        last_noise = 0
        min_noise = 0
        max_noise = 0
        last_time = time.time()
        #last_time
        last_stamp = int(f"{device.get('kismet.device.base.last_time', 'N/A')}")
        if (last_stamp > (last_time - resend_time)):
            print("=====")
            str_sig = f"{device.get('kismet.device.base.signal','N/A')}"
            print(str_sig)
            print(len(str_sig))
            if len(str_sig) > 3:
                sig = re.split(",",re.split("':", str_sig)[4])[0]
                last_noise = re.split(",",re.split("':", str_sig)[3])[0]
                min_noise = re.split(",",re.split("':", str_sig)[5])[0]
                max_noise = re.split(",",re.split("':", str_sig)[7])[0]
                if len(sig)>0:
                    int_sig = int(sig)
                    distance,min_dist, max_dist = self.estimate_distance(int_sig)
                else:
                    distance = 0
                    min_dist = 0
                    max_dist = 0
            else:
                sig = 0
                distance = 0
                min_dist = 0
                max_dist = 0
                last_noise = 0
                min_noise = 0
                max_noise = 0
            first_stamp = int(f"{device.get('kismet.device.base.first_time', 'N/A')}")
            last_stamp = int(f"{device.get('kismet.device.base.last_time', 'N/A')}")
            last_send = last_stamp
            
            data = {
            "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdfaWQiOiJERU5DSVRZIiwiaWF0IjoxNzI1NTI3NzY0fQ.1X0pGlp5MEB72489yGXN2re9jTF9B6HyJuxE054Bcsk",
            "device_id": device_id,
            "raw_data" : [{
            "type":device.get('kismet.device.base.type', 'N/A'),
            "channel":device.get('kismet.device.base.channel', 'N/A'),
            "use": "",
            "bitrate": "",
            "active": "",
            "frequency-known": device.get('kismet.device.base.frequency', 'N/A'),
            "beacon-seen": datetime.fromtimestamp(first_stamp).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "address": device.get('kismet.device.base.macaddr', 'N/A'),
            "networl-ssid": device.get('kismet.device.base.name', 'N/A'),
            "last-beacon": datetime.fromtimestamp(last_stamp).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "beacon-strength": sig,
            "signal-to-noise": "",
            "ssid-source": "",
            "network-station-count": "",
            "use-of-freq": "",
            "use-of-traffic": "",
            "noise-floor": "",
            "frequency-station-count": "",
            "manuf": device.get('kismet.device.base.manuf', 'N/A'),
            "last_noise": last_noise,
            "min_noise": min_noise,
            "max_noise": max_noise}
            ]
            }
            
            try:
                #print(data)        
            
                response = requests.post(url_data, headers=headers_data, json=data)
                print("Status Code", response.status_code)
                print("JSON Response ", response.json())
                print(response)     
            
                print(f"Data submitted successfully ")
            except requests.exceptions.RequestException as e:
                print(f"Failed to submit data ")
    
    def timer(self):
        global jam

        #print(datetime.datetime.now())
        self.lbl_conval1['text'] = ": " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        if self.connect():
            self.lbl_conval['text'] = ": Connected"
            self.lbl_macval['text'] = ": " + str(self.get_mac_address())
            if (self.get_device_id()):
                self.lbl_batu['text'] = ": " + device_id
                self.lbl_cy['text'] = ": ID registered"
                #lbl_conval1
                print("mac address registered")
                
                devices_data = self.get_devices()
                if devices_data:
                    for device in devices_data:
                        self.submit_device_data(device)
                    self.lbl_val['text'] = ": " + datetime.fromtimestamp(last_send).strftime('%Y-%m-%d %H:%M:%S')
                
                    print("last_send: ")
                    print(last_send)
            else:
                self.lbl_batu['text'] = ": No Device ID"
                self.lbl_cy['text'] = ": Not assign"
                self.lbl_val['text'] = ": 00:00:00"
                print("mac address not registered")
            
            print("Connected")
        else:
            self.lbl_conval['text'] = ": Connection loss"
            print("connection loss")
        self.delete_old_file()
            
        current_time = datetime.now()
        if jam != current_time.hour:
            jam = current_time.hour            

        self.window.after(resend_time * 1000, self.timer)
        

        
    def connect(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host) #Python 3.x           
            return True
        except:
            return False

# Create a window and pass it to the Application object
App(tkinter.Tk(), "GUI IoT Measurement. 1.0")
