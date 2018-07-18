#! /usr/bin/python
# Based on
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

import os
from gps import *
from time import *
import time
import threading
import json
import datetime
from time import sleep
from time import gmtime, strftime
import psutil
import colorsys
import os
import sys, socket
import subprocess

# Time
start = time.time()
currenttime= strftime("%Y-%m-%d %H:%M:%S",gmtime())
gpsd = None

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      if gpsd.fix.latitude > 0:
        external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
        socket_family = socket.AF_INET
        host = os.uname()[1]
        ipaddress = IP_address()
        uniqueid = 'gps_uuid_{0}'.format(strftime("%Y%m%d%H%M%S",gmtime()))
        usage = psutil.disk_usage("/")
        mem = psutil.virtual_memory()
        diskrootfree =  "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
        mempercent = mem.percent
        cpuTemp=int(float(getCPUtemperature()))

        row = { 'latitude': str(gpsd.fix.latitude),
         'longitude': str(gpsd.fix.longitude),
         'uniqueid': uniqueid,
         'memory': mempercent,
         'diskfree': diskrootfree,
         'ts': currenttime,
         'host': host,
         'cputemp': round(cpuTemp,2),
         'ipaddress': ipaddress,
         'utc': str(gpsd.utc),
         'time':   str(gpsd.fix.time),
         'altitude': str(gpsd.fix.altitude),
         'eps': str(gpsd.fix.eps),
         'epx': str(gpsd.fix.epx),
         'epv': str(gpsd.fix.epv),
         'ept': str(gpsd.fix.ept),
         'epc': str(gpsd.fix.epc),
         'epd': str(gpsd.fix.epd),
         'epy': str(gpsd.fix.epy),
         'speed': str(gpsd.fix.speed),
         'climb': str(gpsd.fix.climb),
         'track': str(gpsd.fix.track),
         'mode': str(gpsd.fix.mode)}

        json_string = json.dumps(row)
	print(json_string)
        #print(str( gpsd.satellites ) )
        #time.sleep(1)
        sys.exit(0)

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
