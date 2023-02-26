#!/bin/python3
import requests
import sys
import time
import os
from fritzconnection.lib.fritzstatus import FritzStatus

DDNSS_USERNAME= os.environ["DDNSS_USERNAME"]
DDNSS_PASSWORD = os.environ["DDNSS_PASSWORD"]
DDNSS_DOMAIN = os.environ["DDNSS_DOMAIN"]

LOOP = True
SLEEP_TIME = 600

ip = ""
ipv6 = ""

while (LOOP):
    old_ip = ip
    old_ipv6 = ipv6
    get_failed = False
    try:
        fc = FritzStatus(address='192.168.188.1')
        ip = fc.external_ip
        ipv6 = fc.external_ipv6
    except Error as e:
        sys.stderr.write("Error retrieving external IP from fritzbox:")
        sys.stderr.write(e)
        get_failed = True

    if not get_failed and ((old_ip != ip) or (old_ipv6 != old_ipv6)):
        updateurl= f"https://www.ddnss.de/upd.php?user={DDNSS_USERNAME}&pwd={DDNSS_PASSWORD}&host={DDNSS_DOMAIN}&ip={ip}&ip6={ipv6}"
        try:
            r = requests.put(updateurl)
            if r: 
                sys.stdout.write(f"Successfully updated IP Address {ip} and IPv6 Address {ipv6}")
            else:
                raise ConnectionError(f"Updadte failed, Code {r.status_code}")
        except Error as e:
            sys.stderr.write("Error updateing the DynDNS entry:")
            sys.stderr.write(e)

    time.sleep(SLEEP_TIME)