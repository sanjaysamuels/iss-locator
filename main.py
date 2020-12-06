import requests
from datetime import datetime
import time
import smtplib

# Please edit the below fields with your latitude, longitude, email and its password
MY_LAT = 8.186480
MY_LONG = 77.430923
YOUR_EMAIL = "xyz@email.com"
YOUR_PASSWORD = "password"

# Make connection with ISS API
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# Make connection with sunrise, sunset API
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()


# Function to check if ISS position within +5 or -5 degrees.
def check_iss_near(iss_lat, iss_lon, my_lat,my_lon):
    if my_lat-5 <= iss_lat <= my_lat+5 and my_lon-5 < iss_lon < my_lon+5:
        return True


# Function to check if it is dark or not
def check_night_time(set,rise,hour):
    if hour >= set or hour <= rise:
        return True


# Code to check for every minute if the ISS is close to your current position when it is dark
while True:
    time.sleep(60)
    if check_iss_near(iss_latitude, iss_longitude, MY_LAT, MY_LONG) and check_night_time(sunset, sunrise,time_now.hour):
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=YOUR_EMAIL, password=YOUR_PASSWORD)
        connection.sendmail(from_addr=YOUR_EMAIL,
                            to_addrs=YOUR_EMAIL,
                            msg="Subject: ISS ALERT! \n\n Look to the stars, the ISS is near you!")
        connection.close()
    else:
        print("ni")



