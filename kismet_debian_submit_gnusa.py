import requests
import re
import numpy as np
import uuid
import time
#import json
from datetime import datetime

device_id = "GAI-DENCITY.2408.00001"
KISMET_USER = "USER_KISMET"
KISMET_PASSWORD = "PASSWORD_KISMET"

# URL Kismet API

KISMET_URL = f"http://{KISMET_USER}:{KISMET_PASSWORD}@localhost:2501"
api_key = "D80B96E4D7E4614D9926A0BAD9C9B6F2"         # Ganti dengan API key Anda

# Header untuk otorisasi
headers1 = {
    "Authorization": f"Basic {api_key}"
}
headers = {"Content-Type": "application/json; charset=utf-8",'uspw': '{"user":"admin@playup.com","pass":"playup123"}'}
# Endpoint untuk mendapatkan perangkat yang terdeteksi
#DEVICES_ENDPOINT = "/devices/views/physdevices.json"
DEVICES_ENDPOINT = "/devices/last-time/0/devices.json"
# D80B96E4D7E4614D9926A0BAD9C9B6F2
# URL PHP script
PHP_URL = "https://produk-inovatif.com/latihan/wifi/submit_data.php"
url = 'https://adm-iot.gnusa.id/service/device_transmit'
# Header untuk otorisasi
headers1 = {
    "Authorization": f"Basic {api_key}"
}

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

def submit_device_data_print(device):
    mac_address = uuid.getnode()
    mac_address_id = (':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])).upper()

    #print('mac_address': device['kismet.device.base.macaddr')
    #print("=" * 10)
    print(f"Device Name: {device.get('kismet.device.base.name', 'N/A')}")
    print(f"MAC Address: {device.get('kismet.device.base.macaddr', 'N/A')}")
    print(f"Type: {device.get('kismet.device.base.type', 'N/A')}")
    print(f"First Seen: {device.get('kismet.device.base.first_time', 'N/A')}")
    print(f"Last Seen: {device.get('kismet.device.base.last_time', 'N/A')}")
    
    first_stamp = int(f"{device.get('kismet.device.base.first_time', 'N/A')}")
    print("----")
    print(first_stamp)
    print(datetime.fromtimestamp(first_stamp))
    print("====")
    
    #print(type({device.get['kismet.device.base.signal']['kismet.common.signal.last_signal']}))
    str_sig = f"{device.get('kismet.device.base.signal','N/A')}"
    if len(str_sig) > 0:
        sig = re.split(",",re.split("':", str_sig)[4])[0]
        if len(sig)>0:
            int_sig = int(sig)
            distance,min_dist, max_dist = estimate_distance(int_sig)
    print('--==--')
    print(str_sig)
    print(sig)
    print(distance)
    #print(x2)
    print('--==--')
    #sig_dict = json.loads(str_sig)
    #print(type(dict_sig))
    #print(dict_sig)
    print(f"Signal Strength: {sig}")
    print(f"Manufacturer: {device.get('kismet.device.base.manuf', 'N/A')}")
    print(f"Frequency: {device.get('kismet.device.base.frequency', 'N/A')}")
    print("-" * 40)
    
def submit_device_data(device):
    mac_address = uuid.getnode()
    mac_address_id = (':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])).upper()

    str_sig = f"{device.get('kismet.device.base.signal','N/A')}"
    #print(str_sig)
    #print(len(str_sig))
    if len(str_sig) > 0:
        sig = re.split(",",re.split("':", str_sig)[4])[0]
        last_noise = re.split(",",re.split("':", str_sig)[3])[0]
        min_noise = re.split(",",re.split("':", str_sig)[5])[0]
        max_noise = re.split(",",re.split("':", str_sig)[7])[0]
        if len(sig)>0:
            int_sig = int(sig)
            distance,min_dist, max_dist = estimate_distance(int_sig)
        
    first_stamp = int(f"{device.get('kismet.device.base.first_time', 'N/A')}")
    last_stamp = int(f"{device.get('kismet.device.base.last_time', 'N/A')}")
    #print('first_stamp: ')
    #print(first_stamp)
    #print(type(first_stamp))
    #dt = datetime.fromtimestamp(ts)
    
    data = {
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
    
    payload = {
        "mac_address": device.get('kismet.device.base.macaddr', 'N/A'),
        "device_name": device.get('kismet.device.base.name', 'N/A'),
        "type": device.get('kismet.device.base.type', 'N/A'),
        "first_seen": datetime.fromtimestamp(first_stamp),
        "last_seen": datetime.fromtimestamp(last_stamp),
        "strength_sig": sig,
        "distance": distance,
        "manufacturer": device.get('kismet.device.base.manuf', 'N/A'),
        "frequency": device.get('kismet.device.base.frequency', 'N/A')
    }
    try:
        print(data)
        #print(headers)
        
        response = requests.post(url, headers=headers, json=data)
        print("Status Code", response.status_code)
        print("JSON Response ", response.json())
        print(response)
        
        #response = requests.post(PHP_URL, data=payload)
        #print(response)
        #response.raise_for_status()
        print(f"Data submitted successfully for MAC: {payload['mac_address']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to submit data for MAC: {payload['mac_address']} - {e}")

def main():
    devices_data = get_devices()
    #print(devices_data)
    if devices_data:
        for device in devices_data:
            #print("----")
            #print(device)
            submit_device_data(device)
            #submit_device_data_print(device)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
