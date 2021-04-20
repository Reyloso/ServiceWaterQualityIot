#-*- coding: utf-8 -*-
#libraries
import serial
import time
import json
import ast
import socket
import datetime
import pytz
from pubnub_config import pubnubClient
from config import (API_URL, API_SELF_DEVICE_PASSWORD, API_SELF_DEVICE_USERNAME, API_LOGIN_URL, COM_PORT, API_SEND_DATA_URL)
from request import post_data
from influx_config import ifclient
from mongo_config import con

# pubnubconfig variables
subscribe_key = None
publish_key = None
uuid = None
CHANNEL = None

#api login token
token = None

pubnub = pubnubClient()
db = con.waterqualityiot


def login():
    global token, subscribe_key, publish_key, uuid, CHANNEL
    data = post_data(API_LOGIN_URL,body={'username':API_SELF_DEVICE_USERNAME, 'password':API_SELF_DEVICE_PASSWORD})
    token = data['data']
    subscribe_key = data['infodevice']['suscribe_key_pubnub']
    publish_key = data['infodevice']['publish_key_pubnub']
    uuid = data['infodevice']['uuid_key_pubnub']
    CHANNEL = data['infodevice']['channel_pubnub']
    pubnub.pubnub_connection(subscribe_key, publish_key, uuid, CHANNEL)
    print("dispositivo auntenticado")

def sendDataToApi(data):
    response = post_data(API_SEND_DATA_URL, body=json.dumps(data), headers= {"Authorization": "Bearer %s" %token,"Content-Type": "application/json"})
    # print(response)
        
        
def getTime():
    date_time = datetime.datetime.now(pytz.timezone('America/Bogota'))
    date_time = date_time.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time


def IsInternetUp():
    testConn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        # print("comprobando conexion a internet")
        testConn.connect(('google.com.co', 80))
        testConn.close()
        # print("conectado a internet")
        return True
    except:
        # print("Lo siento, pero no se ha podido establecer la conexión.")
        testConn.close()
        return False


def conectSerialWithPort():
    try:
        ser = serial.Serial(COM_PORT, 9600, timeout=20)
        return ser
    except:
        print("no se pudo lograr conexion serial")
        return None

ser = conectSerialWithPort()
flat = True
while 1:
    if ser:
        if ser.read():
           #if IsInternetUp():
            if flat:
                try:
                    #se lee el puerto serial
                    data = ser.readline()
                    # print("antes de json ", data.decode("utf-8"))
                    data_nojson = data.decode("utf-8")
                    datadecode = json.loads(data.decode("utf-8"))
                    # datadecode = json.dumps(datadecode)
                    # print("data decodificada", datadecode)
                    datadecode['date_time'] = str(getTime())
                    
                    # se verifica si esta autenticado
                    if token is None:
                        print("auntenticando dispositivo")
                        login()
                    else:
                        print("enviando data via api-rest")
                        sendDataToApi(datadecode)
                                    
                    if subscribe_key is not None:
                        print("mandar a pubnub")
                        pubnub.pubnub_publish(datadecode)

                        
                    datadecode['send_cloud'] = True
                    
                    if con:
                        print("Conectado a mongo")
                        collection = db.medicion
                        print("consultando si hay datos pendientes para enviar a la nube")
                        querySendCloud = { "send_cloud": False }
                        queryConfirmSendCloud ={ "$set": {"send_cloud":True }}
                        data_send = collection.count_documents(querySendCloud, limit = 1)
                        #print(data_send)
                        data_cloud = []
                        if data_send > 0:
                        	print("si encontró elementos pendientes por enviar")
                        	data_send = collection.find(querySendCloud)
                        	for key in data_send:
                        		data_cloud.append(key)
                        	print(data_cloud)
                        	
                        	#collection.update_many(querySendCloud,queryConfirmSendCloud)
                        else:
                        	print("no hay elementos pendientes por enviar")
                        
                        listamedicion = [(datadecode)]
                        for lista in listamedicion:
                        	collection.insert_one(lista)
                        print("insertando data en mongodb") 
                except Exception as e:
                    print(e)
                    time.sleep(1)
            else:
                try:
                    if con:
                    	print("no hay internet insertando en mongo")
                    	data = ser.readline()
                    	data_nojson = data.decode("utf-8")
                    	datadecode = json.loads(data.decode("utf-8"))
                    	datadecode['date_time'] = str(getTime())
                    	datadecode['send_cloud'] = False
                    	print("conectando con mongodb")
                    	collection = db.medicion
                    	listamedicion = [(datadecode)]
                    	for lista in listamedicion:
                    	    collection.insert_one(lista)
                    	print("insertando data en mongodb")
                
                except Exception as e:
                    print(e)
                    time.sleep(1)
