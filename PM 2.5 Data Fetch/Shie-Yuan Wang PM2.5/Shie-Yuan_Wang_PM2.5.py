#!/usr/bin/env python3
import MySQLdb, time, logging
from datetime import datetime
import paho.mqtt.client as mqtt

#Starting configuration for Database Connection
hostDB = "host"
userDB = "user"
passDB = "pass"
database = "db"

#Starting configuration for paho-mqtt  
user = "user"
passw = "pass"
MQTT_Broker = "broker"
MQTT_Port = port
Keep_Alive_Interval = 45
MQTT_Topic = "topic"

#Subscribe to all Sensors
def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_Topic)
  
#Save data into DB Table
def on_message(client, userdata, msg):
    # This is the Master Call for saving MQTT Data into DB
    # For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
    #Changing filename and formatting for logging file
    fetch_logfile = logging.FileHandler("./logfile/WangPM2.5_fetch_" + datetime.now().strftime("%Y-%m-%d") + ".log", "a")
    fetch_formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
    fetch_logfile.setFormatter(fetch_formatter)
    logs = logging.getLogger()
    logs.setLevel(logging.DEBUG)
    
    for hdlr in logs.handlers[:]:
        logs.removeHandler(hdlr)
    logs.addHandler(fetch_logfile)
    
    logs.info ("MQTT Data Received for: " + msg.payload.decode("utf-8"))
    #logs.info ("MQTT Topic: " + msg.topic)  
    PM25_data = msg.payload.decode("utf-8").split()
    #Format: Location, Date, Time, Avg. PM2.5
    times = datetime.combine(datetime.strptime(PM25_data[1], "%Y-%m-%d"), datetime.strptime(PM25_data[2], "%H:%M:%S").time())
    
    myConnection = MySQLdb.connect( host=hostDB, user=userDB, passwd=passDB, db=database, use_unicode=True, charset="utf8" )
    myCursor = myConnection.cursor()
    myCursor.execute( "INSERT IGNORE INTO `Wang_device_data` (`location`, `time`, `pm25`) VALUES (\"" + PM25_data[0] + "\",\"" + str(times) + "\",\'" + PM25_data[3] + "\');")
    myConnection.commit()
    myCursor.close()
    myConnection.close()
  
  
def on_subscribe(mosq, obj, mid, granted_qos):
    pass

client = mqtt.Client()

# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe

# Connect
client.username_pw_set(username=user, password=passw)
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
client.loop_forever()
