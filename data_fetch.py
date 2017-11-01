#!/usr/bin/env python3
import requests, json, MySQLdb, time, logging
from datetime import datetime

#Redirect logging output to a file
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG, filename=str(datetime.now().date()) + "_datafetch.log", filemode="a+", format="%(asctime)-8s %(levelname)-8s %(message)s", datefmt='%I:%M:%S')

  logging.info("Program started to run.....")

  #Starting configuration for Database Connection
  logging.info("Using MySQLdb")
  hostname = "172.16.1.200"
  username = "phua"
  password = "wilbert612"
  database = "phua"
  
  while True:
    logging.info("Trying to retrieve data......")
    #Trying to access data from the link (.json format)
    r = requests.get("https://ab2.edimaxcloud.com/devices?token=c58affa8-b74e-4341-a020-82b4ba776a69", verify=False);
    #Continue if status is normal
    logging.info("Status code: " + str(r.status_code))
    if (r.status_code/100) == 2:
      #Tryingto connect to database server
      myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database, use_unicode=True, charset="utf8" )
      myCursor = myConnection.cursor()
      response_obj = json.loads(r.text);
      
      #Check whether data sent has "ok" or "fail" status
      logging.info("Response code: " + str(response_obj["status"]))
      if str(response_obj["status"]) == "ok":
        logging.info("Number of data received: " + str(len(response_obj["devices"])))
        for x in response_obj["devices"]:
          myCursor.execute( "INSERT IGNORE INTO `devices_info` (`id`, `name`, `lat`, `lon`) VALUES (\"" + x["id"] + "\",\"" + x["name"] + "\",\'" + str(x["lat"]) + "\',\'" + str(x["lon"]) + "\');")
          myCursor.execute( "INSERT IGNORE INTO `devices_data` (`id`, `pm25`, `pm10`, `co2`, `hcho`, `tvoc`, `co`, `t`, `h`, `time`, `org`, `area`, `type`) VALUES (\"" + x["id"] + "\",\'" + str(x["pm25"]) + "\',\'" + str(x["pm10"]) + "\',\'" + str(x["co2"]) + "\',\'" + str(x["hcho"]) + "\',\'" + str(x["tvoc"]) + "\',\'" + str(x["co"]) + "\',\'" + str(x["t"]) + "\',\'" + str(x["h"]) + "\',\"" + x["time"] + "\",\"" + x["org"] + "\",\'" + str(x["area"]) + "\',\"" + x["type"] + "\");")
          myConnection.commit()
        logging.info("Data successfully saved into DB")
      else:
        logging.error("Json data status fail")

      myCursor.close()
      myConnection.close()
      #Wait for 5 minutes before trying to retrieve next data
      time.sleep (300)
    else:
      logging.error("Data retrieval failed")
      #Wait for 100 seconds to retry data retrieval
      time.sleep (100)
