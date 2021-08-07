import time

from rofi import Rofi
import os
import subprocess
import re

rofi_menu = Rofi()


CONST_PASSWORD_NEEDED = "Error: Connection activation failed: (7) Secrets were required, but not provided."
CONST_SUCCESSFUL_CONNECTION_KEYWORDS = ["Device", "successfully", "activated", "with"]
CONST_PASSWORD_INCORRECT = "Error: 802-11-wireless-security.psk: property is invalid."


def get_wifi_networks():
    wifi_devices_raw = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'])
    wifi_devices_decoded = wifi_devices_raw.decode("utf-8").strip()
    wifi_list = wifi_devices_decoded.split('\n')
    return wifi_list


def display_nearby_networks(wifi_list):
    index, key = rofi_menu.select('Select wifi', wifi_list)
    return index, key


def connect_to_wifi(wifi_list_index, wifi_list):
    wifi_information = wifi_list[wifi_list_index]
    ssid_to_connect = cleanup_wifi_info_to_ssid(wifi_information)

    try:
        connection_result = subprocess.check_output(['nmcli', 'device', 'wifi', 'connect', ssid_to_connect]).decode(
            "utf-8").strip()
    except:
        exit()

    if CONST_PASSWORD_NEEDED == connection_result:
        check_to_loop = True
        while check_to_loop:
            check_to_loop = False
            password = enter_password()
            os.system("notify-send \"Connecting...\"")
            try:
                connection_result = subprocess.check_output(
                    ['nmcli', 'device', 'wifi', 'connect', ssid_to_connect, 'password', password])
                connection_result = connection_result.decode("utf-8").strip()
            except Exception as e:
                if type(e) == subprocess.CalledProcessError:
                    os.system("notify-send \"Error: Incorrect Password\"")
                    check_to_loop = True
                elif type(e) == TypeError:
                    exit()
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                print(message)
            if all(word in connection_result for word in CONST_SUCCESSFUL_CONNECTION_KEYWORDS):
                os.system("notify-send \"Connected to " + ssid_to_connect + "\"")
                check_to_loop = False
    else:
        os.system("notify-send \"Connected to " + ssid_to_connect + "\"")
        print(connection_result)


def enter_password():
    password = rofi_menu.text_entry("Please enter the password: ")
    return password


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
