#!/usr/bin/env python
import pymongo
from pymongo import MongoClient


MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DB = "waterqualityiot"
MONGO_COLL = "medicion"

# MONGO_USER = "admin"
# MONGO_PSW = "mon2021"

con = MongoClient(MONGO_HOST)

#db = con.MONGO_DB

#collection = db.MONGO_COLL

