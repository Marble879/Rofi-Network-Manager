#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import shlex
import subprocess
import re

DOCUMENTATION = '''
---
module: nmcli
short_description: Wrapper around nmcli executable itself
description:
    - Execute nmcli command to gather information about network manager
      devices.
'''


NMCLI_FIELDS = {
    'nm': "RUNNING STATE WIFI-HARDWARE WIFI WWAN-HARDWARE WWAN".split(),
    'con': "NAME UUID TYPE TIMESTAMP-REAL".split(),
    'dev': "DEVICE TYPE STATE".split(),
    'con list': (
        "connection,802-3-ethernet,802-1x,802-11-wireless," +
        "802-11-wireless-security,ipv4,ipv6,serial,ppp,pppoe," +
        "gsm,cdma,bluetooth,802-11-olpc-mesh,vpn,infiniband,bond," +
        "vlan").split(","),
    'dev wifi': ("SSID BSSID MODE FREQ RATE SIGNAL SECURITY WPA-FLAGS RSN-FLAGS DEVICE ACTIVE DBUS-PATH").split(),
    'dev list': ("GENERAL CAPABILITIES BOND VLAN CONNECTIONS WIFI-PROPERTIES AP WIRED-PROPERTIES IP4 DHCP4 IP6 DHCP6").split(),
    'nm permissions': ("PERMISSION VALUE").split()
}


def shell(args):
    """Execute args and returns status code, stdout and stderr

    Any exceptions in running subprocess are allowed to raise to caller
    """
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    retcode = process.returncode

    return retcode, stdout, stderr


def nmcli(obj, command=None, fields=None, multiline=False):
    """Wraps nmcli execution"""
    if fields is None:
        fields = NMCLI_FIELDS[obj]

    if "list" in command and "id" in command:
        multiline = True
        fields = NMCLI_FIELDS["%s list" % obj]

    if command:
        if ("%s %s" % (obj,command)) in NMCLI_FIELDS:
            fields=NMCLI_FIELDS[("%s %s" % (obj,command))]

    args = ['nmcli', '--terse', '--fields', ",".join(fields), obj]

    if command:
        args += shlex.split(command)

    retcode, stdout, stderr = shell(args)
    data = []
    if retcode == 0:
        if multiline:
            # prev_field = None
            row = {}
            for line in stdout.split('\n'):
                values = line.split(':', 1)
                if len(values) == 2:
                    multikey, value = values
                    field, prop = multikey.split('.')
                    row[prop] = value
            data.append(row)
        else:
            for line in stdout.split('\n'):
                values = re.split(r'(?<!\\):', line)
                if len(values) == len(fields):
                    row = dict(zip(fields, values))
                    data.append(row)
        return data
    else:
        msg = "nmcli return {0} code. STDERR='{1}'".format(retcode, stderr)
        raise Exception(msg)
