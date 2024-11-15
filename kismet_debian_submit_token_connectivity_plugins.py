import requests
import re
import numpy as np
import uuid
import urllib.request
import time

import os
from os.path import exists
import glob

#import json
from datetime import date
from datetime import datetime
global device_id, resend_time, mac_address_id,resend_time, jam, last_send, file_del_days
mac_address_id = 0
device_id = ""#"DENCITY-Playup.2409.00001"

resend_time = 10
jam = 0
last_send = 0
# hari delete file kismet
file_del_days = 10
bad_chars = ['{', '}', "'"]

KISMET_USER = "KISMET_USER"            # ganti dengan user kismet
KISMET_PASSWORD = "KISMET_PASSWORD"    # ganti dengan password kismet

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



def connect(host='http://google.com'):
        try:
            urllib.request.urlopen(host) #Python 3.x
            return True
        except:
            return False
def estimate_distance(power_received, params=None):
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

def get_device_id_old ():
    global device_id
    data_device ={
    "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdfaWQiOiJERU5DSVRZIiwiaWF0IjoxNzI1NTI3NzY0fQ.1X0pGlp5MEB72489yGXN2re9jTF9B6HyJuxE054Bcsk",
    "mac_address":get_mac_address(),
    "device_type":"Mini PC"}
    
    try:
        response = requests.post(url_regis, headers=headers_regis, json=data_device)
        print("Status Code", response.status_code)
        res_json = response.json()
        print("JSON Response ", res_json)
        device_id = res_json["data"]["device_id"]
        
        print(f"Data get device id successfully")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to get device id")
        return False
    
def get_devices():
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
     
def submit_device_data(device):
    last_time = time.time()
    last_stamp = int(f"{device.get('kismet.device.base.last_time', 'N/A')}")
    
    if (last_stamp < (last_time - resend_time)):        
        str_dot11 = f"{device.get('dot11.device','N/A')}"
        if len(str_dot11) > 3:
            strBSSID = re.split(",",re.split("':", str_dot11)[24])[0]
            for i in bad_chars:
                strBSSID = strBSSID.replace(i, '')
            strBSSID = strBSSID[1:len(strBSSID)]
        str_sig = f"{device.get('kismet.device.base.signal','N/A')}"

        if len(str_sig) > 3:
            sig = re.split(",",re.split("':", str_sig)[2])[0]
            last_noise = re.split(",",re.split("':", str_sig)[3])[0]
            min_noise = re.split(",",re.split("':", str_sig)[5])[0]
            max_noise = re.split(",",re.split("':", str_sig)[7])[0]
            if len(sig)>0:
                int_sig = int(sig)
                distance,min_dist, max_dist = estimate_distance(int_sig)
            else:
                distance = 0
                min_dist = 0
                max_dist = 0
                last_noise = 0
                min_noise = 0
                max_noise = 0
                sig = 0
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
        
        if (strBSSID == "00:00:00:00:00:00") :
            type_device = "Wi-Fi Floating"
            print(strBSSID)
        else:
            type_device = device.get('kismet.device.base.type', 'N/A')
            
        data = {
        "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdfaWQiOiJERU5DSVRZIiwiaWF0IjoxNzI1NTI3NzY0fQ.1X0pGlp5MEB72489yGXN2re9jTF9B6HyJuxE054Bcsk",
        "device_id": device_id,
        "raw_data" : [{
        "type":type_device,
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
        "ssid-source": strBSSID,
        "network-station-count": "",
        "use-of-freq": "",
        "use-of-traffic": "",
        "noise-floor": "",
        "frequency-station-count": "",
        "manuf": device.get('kismet.device.base.manuf', 'N/A'),
        "last_noise": last_noise,
        "min_noise": min_noise,
        "max_noise": max_noise,
        "estimate_distance": distance,
        "min_distance": min_dist,
        "max_distance": max_dist}
        ]
        }
        
        try:        
            response = requests.post(url_data, headers=headers_data, json=data)
            print("Status Code", response.status_code)
            print("JSON Response ", response.json())
            print(response)     
        
            print(f"Data submitted successfully ")
        except requests.exceptions.RequestException as e:
            print(f"Failed to submit data ")

def get_mac_address():
    global mac_address_id
    mac_address = uuid.getnode()
    mac_addressA = (':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])).upper()
    print("mac")
    print(mac_addressA)
    mac_address_id = mac_addressA
    #mac_address_id = "7C:83:34:BB:74:D1"
    
    return mac_addressA

def get_device_id ():
    global device_id, mac_address_id, macADDR
    
    isExistlog = os.path.exists("macADDR.txt")
    if isExistlog:
        print("MAC ADDR exist")
        f = open("macADDR.txt", "r")
        macADDR = f.readline()
        f.close()
        print(macADDR)
    else:
        print("MAC ADDR not exist")
        macADDR = get_mac_address()
        #f = open("macADDR.txt", "w")
        #f.write(macADDR)
        #f.close()
    
    data_device ={
    "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdfaWQiOiJERU5DSVRZIiwiaWF0IjoxNzI1NTI3NzY0fQ.1X0pGlp5MEB72489yGXN2re9jTF9B6HyJuxE054Bcsk",
    "mac_address":macADDR,
    "device_type":"Mini PC"}
    
    try:
        response = requests.post(url_regis, headers=headers_regis, json=data_device)
        print("Status Code", response.status_code)
        if (int(response.status_code) == 200):
            res_json = response.json()
            # if device id ready, respond
            # {'status': 0, 'message': 'Mac address received', 'data': {'device_id': 'DENCITY-Playup.2409.00005'}}
            
            # if device id not assigmented, respond
            # {'status': 0, 'message': 'Mac address received'}
            print("JSON Response ", res_json)
            if "data" in res_json:
                #print("registered")
                device_id = res_json["data"]["device_id"]               
                
                isExistlog = os.path.exists("macADDR.txt")
                if isExistlog:
                    print("MAC ADDR exist")
                else:
                    print("MAC ADDR not exist")
                    f = open("macADDR.txt", "w")
                    f.write(macADDR)
                    f.close()
                print("Data get device id successfully")
                return True
            else:
                #print("not registered")
                
                return False
            
        
    except requests.exceptions.RequestException as e:
        print("Failed to get device id")
        return False

def delete_old_file():
    #current_time = str(datetime.now().strftime("%Y%m%d"))
        
    os.chdir(path_kismet_data)
        #for fileN in os.listdir(path_kismet_data):
    for fileN in glob.glob("*.kismet"):
            
        x = fileN.split("-")
        #today = datetime.now().strftime("%Y-%m-%d")
        #year = today.year
        date_create = date(int(x[1][0:4]),int(x[1][4:6]),int(x[1][6:9]))            
        get_diff_days = (date.today() - date_create).days
        print("diff_dasy", get_diff_days)
            
        # file_del_days
        if get_diff_days > file_del_days:
            isExistdelKISMET = os.path.exists(path_kismet_data + "/" + fileN)
            if isExistdelKISMET:
                print("hapus data")
                os.remove(path_kismet_data + "/" + fileN)
                    
def main():
    #devices_data = get_devices()
    #print(devices_data)
    if (get_device_id()):
        #print(device_id)
        devices_data = get_devices()
        #print(devices_data)
        if devices_data:
            for device in devices_data:
                print("====>")
                #print(device)
                submit_device_data(device)
        #        submit_device_data(device)
    else:
        print("mac address not registered")
    delete_old_file()
    
if __name__ == "__main__":
    while True:
        if connect():
            main()
        else:
            print("connection loss")
        time.sleep(resend_time)
