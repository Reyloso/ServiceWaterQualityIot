#!/usr/bin/env python
import psutil
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "root"
ifpass = "mon2021"
ifdb   = "waterqualityiot"
ifhost = "127.0.0.1"
ifport = 8086

# collect some stats from psutil
disk = psutil.disk_usage('/')
mem = psutil.virtual_memory()
load = psutil.getloadavg()


# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement