from rofi import Rofi
import os
from NetworkManager import *
import subprocess

#you get the individual lines by .split("\n")
#for the next part there are several options
#they're pretty neatly aligned so you could try to get the string indices of the header row using .find
#and then read from that index for every line
#another option is to use a regular expression
#but maybe you can also split by two spaces (not sure if that always works)


#TODO: move this into a method
rofi = Rofi()

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
    # index, key = quickOptionsTest()
    # print("index: " + str(index) + "\n" + "key: " + str(key))
    #get_wifi_networks()
    #os.system("nmcli device wifi list")
    get_wifi_networks()