#Alex Walters https://github.com/AlexWalters8915 1.0.0
import timezonefinder
import datetime
import pytz
import geopy
import geopy.exc
import csv
import pandas as pd
import os
import pywinauto
from pywinauto.keyboard import send_keys
import time


fields = ['NAME', 'Location']
filename = "FriendTimeFinder"

# Check if file exists create it if it does not
if not os.path.exists(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

#class used to perform the time calcilations
class TimezoneCalculator:
    def __init__(self):
        self.tf = timezonefinder.TimezoneFinder()
        #Note geopy uses a small collection of servers that are donated, Please asign a name to the user agent that is not the same as Friend Time zone calculator
        self.geolocator = geopy.geocoders.Nominatim(user_agent="Friend Time zone calculator")

    def getTime(self, location_name):

            # Get the latitude and longitude of the location based off of the name passed in
            location = self.geolocator.geocode(location_name, timeout=10)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                # Get the timezone name
                timezoneName = self.tf.timezone_at(lng=longitude, lat=latitude)
                if timezoneName:
                    # Get the current time in the timezone
                    timezone = pytz.timezone(timezoneName)
                    curretnTime = datetime.datetime.now(timezone)
                    return curretnTime.strftime('%I:%M:%S %p')
                else:
                    return "Location not found"
            else:
                return "Location not found."

df = pd.read_csv('FriendTimeFinder')
timezoneCalculator = TimezoneCalculator()
print("Add new Friend and time? Y/N")
engage = input()
if engage == "Y" or engage == "y":
    collectedname = input("Friends name:")
    print("Note:Landmarks,cities,states exact address country and other locations all tend to work")
    collectedloc = input("Friends location:")
    mydict = [{'NAME': collectedname, 'Location': collectedloc}]
    with open(filename, 'a', newline='') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        # writing data rows
        writer.writerows(mydict)
    print("Now showing relevent time zones for friends.")
   # df = pd.read_csv('FriendTimeFinder')
    for index, row in df.iterrows():
        location = row['Location']
        #call to time zone calculation
        currentTime = timezoneCalculator.getTime(location)
        # Assign the current time to the 'time' column for the corresponding location
        df.loc[index, 'time'] = currentTime
         #asign the values to the time column
    df = pd.read_csv(filename)

    print(df)
else:
    print("Now showing relevent time zones for friends.")
  #  df = pd.read_csv('FriendTimeFinder')
    for index, row in df.iterrows():
        location = row['Location']
        currentTime = timezoneCalculator.getTime(location)
       #appends new time column to the data frame and displays the times
        df.loc[index, 'time'] = currentTime
    df = pd.read_csv(filename)

    print(df)
