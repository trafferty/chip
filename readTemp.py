#!/usr/bin/python3

import time
import os
import re
import argparse
import sys
import datetime

def readDS18B20(sensor_id):
    if sensor_id is None:
        return None

    dev_file = "/sys/bus/w1/devices/" + sensor_id + "/w1_slave"
    regex = r".*?crc=.*? t=(?P<temp>[0-9]*)"
    attempt = 0

    while(1):
        # /sys/bus/w1/devices/28-0117b241d4ff/w1_slave
        try:
            with open(dev_file, 'r') as dev_file:
                buf = dev_file.read()

            match_set =[x.groupdict() for x in re.finditer(regex, buf, re.DOTALL)]
            if len(match_set) > 0:
                return float(match_set[0]['temp'])/1000.0
        except:
            # ok error, loop it
            pass

        attempt +=  1
        if attempt >= 5:
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='read DS18B20 via device file and return temp')
    parser.add_argument('--sensor_id', type=str, default='28-0117b241d4ff',
                        help='sensor id (under /sys/bus/w1/devices/)')
    parser.add_argument('--output_path', dest='output_path', type=str,
                        help='output path', default='.')
    parser.add_argument('--interval_s', dest='interval_s', type=int,
                        help='interval between reads in sec', default=10)
    args = parser.parse_args()

    dat_file = "%s/temperature_%s.dat" % (args.output_path, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    with open(dat_file, 'w') as temp_file:
       temp_file.write("timestamp, temp (C), temp (F)\n")

    while True:
        temp_C = readDS18B20(args.sensor_id)
        if temp_C != None:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            temp_F = temp_C * (9.0/5.0) + 32
            print("%s: %f C (%f F)" % (ts, temp_C, temp_F))

            with open(dat_file, 'a') as temp_file:
                temp_file.write("%s, %f, %f\n" % (ts, temp_C, temp_F))

        time.sleep(args.interval_s)