#-*- coding: utf-8 -*-
#libraries
import serial
import time
import json
import socket
import datetime
import pytz
from double_quotes_json_parse import double_quotes_parse
from pubnub_config import pubnubClient
from config import (API_URL, API_SELF_DEVICE_PASSWORD, API_SELF_DEVICE_USERNAME, API_LOGIN_URL, COM_PORT, API_SEND_DATA_URL)
from request import post_data
from influx_config import ifclient

# pubnubconfig variables
subscribe_key = None
publish_key = None
uuid = None
CHANNEL = None

#api login token
token = None

pubnub = pubnubClient()


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
    print("antes de aja", data)
    data = double_quotes_parse(data)
    print("data parse" , data)
    response = post_data(API_SEND_DATA_URL, body=data, headers= {"Authorization": "Bearer %s" %token,"Content-Type": "application/json"})
    print(response)
        
        
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

# redis = connectRedisLocalDatabase()

def conectSerialWithPort():
    try:
        ser = serial.Serial(COM_PORT, 9600, timeout=20)
        return ser
    except:
        print("no se pudo lograr conexion serial")
        return None

ser = conectSerialWithPort()

while 1:
    if ser.read():
        if IsInternetUp():
            # print("guardar en la nube")
            try:
                #se lee el puerto serial
                data = ser.readline()
                #print("antes de ",data)
                datadecode = json.loads(data)
                datadecode['date_time'] = str(getTime())
                
                # se verifica si esta autenticado
                if token is None:
                    print("auntenticando dispositivo")
                    login()
                else:
                    print("enviando data via api-rest")
                    sendDataToApi(datadecode)
                
                #print(datadecode)
               
                # print(data_format)
                if subscribe_key is not None:
                    print("mandar a pubnub")
                    #pubnub.pubnub_publish(datadecode)
                    
                datadecode['send_cloud'] = True
                
                if ifclient:
                    
                        
                    #ifclient.write_points(dict(datadecode))
                    print("insertado en influx")
                # print(ser.readline().decode('utf-8'))
            except Exception as e:
                print(e)
                time.sleep(1)
        else:
            try:
                data = ser.readline()
                # print(data)
                datadecode = json.loads(data)
                datadecode['date_time'] = str(getTime())
                datadecode['send_cloud'] = False
                print("guardar en influx db")
                if ifclient:
                    data = [{
                        "measurement":"measurement",
                        "data":datadecode}]
                    ifclient.write_points(data)
                    print("insertado en influx")
                # print(ser.readline().decode('utf-8'))
            except Exception as e:
                print(e)
                time.sleep(1)
#  