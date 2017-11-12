#!/usr/bin/env python3
import requests, json, MySQLdb, time, logging
from datetime import datetime

#Redirect logging output to a file
if __name__ == "__main__":
  #logging.basicConfig(level=logging.DEBUG, filename="fetching" + datetime.date() + ".log", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
  
  #Starting configuration for Database Connection
  hostname = "host"
  username = "user"
  password = "pass"
  database = "db"
  
  while True:
    #Changing filename and formatting for logging file
    fetch_logfile = logging.FileHandler("fetching_" + datetime.now().strftime("%Y-%m-%d") + ".log", "a")
    fetch_formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
    fetch_logfile.setFormatter(fetch_formatter)
    logs = logging.getLogger()
    logs.setLevel(logging.DEBUG)

    for hdlr in logs.handlers[:]:
      logs.removeHandler(hdlr)
    logs.addHandler(fetch_logfile)

    logs.info("Trying to retrieve data......")
    #Trying to access data from the link (.json format)
    try:
      r = requests.get("url link", verify=False);
    except:
      logs.error("Data request failed. Program will sleep for a while")
      time.sleep(301)
      continue
    
#Continue if status is normal
    logs.info("Status code: " + str(r.status_code))
    if (r.status_code/100) == 2:
      #Tryingto connect to database server
      myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database, use_unicode=True, charset="utf8" )
      myCursor = myConnection.cursor()
      response_obj = json.loads(r.text);
      
      #Check whether data sent has "ok" or "fail" status
      logs.info("Response code: " + str(response_obj["status"]))
      if str(response_obj["status"]) == "ok":
        logs.info("Number of data received: " + str(len(response_obj["devices"])))
        for x in response_obj["devices"]:
          myCursor.execute( "INSERT IGNORE INTO `devices_info` (`id`, `name`, `lat`, `lon`) VALUES (\"" + x["id"] + "\",\"" + x["name"] + "\",\'" + str(x["lat"]) + "\',\'" + str(x["lon"]) + "\');")
          myCursor.execute( "INSERT IGNORE INTO `devices_data` (`id`, `pm25`, `pm10`, `co2`, `hcho`, `tvoc`, `co`, `t`, `h`, `time`, `org`, `area`, `type`) VALUES (\"" + x["id"] + "\",\'" + str(x["pm25"]) + "\',\'" + str(x["pm10"]) + "\',\'" + str(x["co2"]) + "\',\'" + str(x["hcho"]) + "\',\'" + str(x["tvoc"]) + "\',\'" + str(x["co"]) + "\',\'" + str(x["t"]) + "\',\'" + str(x["h"]) + "\',\"" + x["time"] + "\",\"" + x["org"] + "\",\'" + str(x["area"]) + "\',\"" + x["type"] + "\");")
          myConnection.commit()
        logs.info("Data successfully saved into DB")
      else:
        logs.error("Json data status fail")

      myCursor.close()
      myConnection.close()
      #Wait for 5 minutes before trying to retrieve next data
      time.sleep (301)
    else:
      logs.error("Data retrieval failed")
      #Wait for 100 seconds to retry data retrieval
      time.sleep (301)
