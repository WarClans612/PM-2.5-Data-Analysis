#!/usr/bin/env python3
import requests, json, MySQLdb, time, logging
from datetime import datetime

#Redirect logging output to a file
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG, filename=str(datetime.now().date()) + "_logfile.log", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")

  logging.info("Program started to run.....")

  #Starting configuration for Database Connection
  logging.info("Using MySQLdb")
  hostname = "host"
  username = "user"
  password = "passwd"
  database = "db"
  myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database, use_unicode=True, charset="utf8" )
  myCursor = myConnection.cursor()
  
  while True:
    logging.info("Trying to retrieve data......")
    #Trying to access data from the link (.json format)
    r = requests.get("https://ab2.edimaxcloud.com/devices?token=c58affa8-b74e-4341-a020-82b4ba776a69", verify=False);
    #Continue if status is normal
    logging.info("Status code: " + str(r.status_code))
    if (r.status_code/100) == 2:
      response_obj = json.loads(r.text);
      
      #Check whether data sent has "ok" or "fail" status
      logging.info("Response code: " + str(response_obj["status"]))
      if str(response_obj["status"]) == "ok":
        logging.info("Number of data received: " + str(len(response_obj["devices"])))
        for x in response_obj["devices"]:
          myCursor.execute( "INSERT IGNORE INTO `devices_info` (`id`, `name`, `lat`, `lon`) VALUES (\"" + 
            x["id"] + "\",\"" + x["name"] + "\",\'" + str(x["lat"]) + "\',\'" + str(x["lon"]) + "\');")
          myConnection.commit()
        logging.info("Data successfully saved....")

      #Wait for 5 minutes before trying to retrieve next data
      time.sleep (300)
    else:
      logging.info("Data retrieval failed....")
      #Wait for 100 seconds to retry data retrieval
      time.sleep (100)
  
  myCursor.close()
  myConnection.close()
  
