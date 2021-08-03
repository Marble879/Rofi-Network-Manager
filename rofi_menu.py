from rofi import Rofi
import os
import subprocess

def get_wifi_networks():
    wifi_devices_raw = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'])
    wifi_devices_decoded = wifi_devices_raw.decode("utf-8")
    wifi_list = wifi_devices_decoded.split('\n')
    return wifi_list





def quick_options_test():
    options = ['Red', 'Green', 'Blue', 'White', 'Silver', 'Black', 'Other']
    index, key = rofi.select('What colour car do you drive?', options)
    return index, key

if __name__ == '__main__':
    get_wifi_networks()