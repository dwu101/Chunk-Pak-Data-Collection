
import gspread
import time
import requests
from oauth2client.service_account import ServiceAccountCredentials
from settings import PurpleAirKey, PurpleAirSensorIndex13, PurpleAirSensorIndex4, floor_13_id, floor_4_id, floor_13_fileID, floor_4_fileID
from datetime import datetime
from create_files import create_files

folderIds = [floor_4_id, floor_13_id]

fileIds= [floor_4_fileID,floor_13_fileID]
newMonthDetected = False
minutesSinceReset = 0
week_num = 1

while True:

    try:
        credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json")
        client = gspread.authorize(credential)
        headers = {
            "X-API-Key": PurpleAirKey
        }
        
        timenow = datetime.now().strftime("%m/%d/%Y %H:%M")
        day = timenow[3:5]
        month = timenow[0:2]
        year = timenow[6:10]
        PurpleAir13 = requests.request("GET", "https://api.purpleair.com/v1/sensors/{x}".format(x = PurpleAirSensorIndex13), headers=headers, )

        row1 = [timenow,PurpleAir13.json()["sensor"]["name"],PurpleAir13.json()["sensor"]["pm1.0"],
            PurpleAir13.json()["sensor"]["pm2.5"], PurpleAir13.json()["sensor"]["stats"]["pm2.5_24hour"],
            PurpleAir13.json()["sensor"]["pm10.0"]
            ]

        PurpleAir4 = requests.request("GET", "https://api.purpleair.com/v1/sensors/{x}".format(x = PurpleAirSensorIndex4), headers=headers, )
        
        row2 = [timenow,PurpleAir4.json()["sensor"]["name"],PurpleAir4.json()["sensor"]["pm1.0"],
            PurpleAir4.json()["sensor"]["pm2.5"], PurpleAir4.json()["sensor"]["stats"]["pm2.5_24hour"],
            PurpleAir4.json()["sensor"]["pm10.0"]
            ]
        

        if day == "01" and not newMonthDetected:
            week_num = 1
            minutesSinceReset = 0
            for i in range(len(folderIds)):
                fileIds[i] = create_files(folderIds[i], month, year)
            
            newMonthDetected = True
        
        if day == "02":
            newMonthDetected = False

        floor_4 = client.open_by_key(fileIds[0]).worksheet("Week {x} AQ".format(x = week_num)) 
        floor_13 = client.open_by_key(fileIds[1]).worksheet("Week {x} AQ".format(x = week_num))

        minutesSinceReset +=1

        if minutesSinceReset == 10080: #minutes in a week 
            week_num+=1
            minutesSinceReset = 0 

        floor_4.insert_row(row1, 3)  
        floor_13.insert_row(row2, 3)
        time.sleep(60)
        
    except:
        print("ERROR")
        time.sleep(60)
