from rofi import Rofi
import os
import subprocess
import re


def get_wifi_networks():
    wifi_devices_raw = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'])
    wifi_devices_decoded = wifi_devices_raw.decode("utf-8")
    wifi_list = wifi_devices_decoded.split('\n')
    return wifi_list


def display_nearby_networks(wifi_list):
    rofi_menu = Rofi()
    index, key = rofi_menu.select('Select wifi', wifi_list)
    return index, key


def connect_to_wifi(wifi_list_index, wifi_list):
    wifi_information = wifi_list[wifi_list_index]
    ssid_to_connect = cleanup_wifi_info_to_ssid(wifi_information)
    os.system("nmcli device wifi connect " + ssid_to_connect)


def cleanup_wifi_info_to_ssid(wifi_to_cleanup):
    mac_address_pattern = r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}"

    wifi_to_cleanup = re.sub(mac_address_pattern, '', wifi_to_cleanup)
    wifi_to_cleanup = wifi_to_cleanup.replace("*", "")
    wifi_to_cleanup = wifi_to_cleanup.strip()

    ssid = wifi_to_cleanup.split(" ")[0]

    return ssid


if __name__ == '__main__':
    wifi_list = get_wifi_networks()
    index, key = display_nearby_networks(wifi_list)
    connect_to_wifi(index, wifi_list)
