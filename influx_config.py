#!/usr/bin/env python
import psutil
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "root"
ifpass = "root"
ifdb   = "waterqualityiot"
ifhost = "127.0.0.1"
ifport = 8086

# collect some stats from psutil
disk = psutil.disk_usage('/')
mem = psutil.virtual_memory()
load = psutil.getloadavg()


# connect to influx
ifclient = InfluxDBClient(host=ifhost,port=ifport,username=ifuser,password=ifpass)
ifclient.switch_database(ifdb)

# write the measurement