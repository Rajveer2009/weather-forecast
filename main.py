import time
import requests
import geocoder
import datetime
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "OPENWEATHERMAP API KEY"


def get_time(timestamp):
    datetime_obj = datetime.datetime.fromtimestamp(int(timestamp))
    human_time = datetime_obj.strftime("%H:%M")
    return human_time


def get_weather(postal_code):

    postal_code = int(postal_code)
    g = geocoder.arcgis(postal_code)
    lat, lng = g.latlng
    latitude = round(lat, 4)
    longitude = round(lng, 4)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    raw_weather_data = response.json()

    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    name = raw_weather_data["name"]
    weather_main = raw_weather_data["weather"][0]["main"]
    temperature = str(round(raw_weather_data["main"]["temp"] - 273.15)) + "°C"
    wind_speed = round(raw_weather_data["wind"]["speed"])
    humidity = str(raw_weather_data["main"]["humidity"]) + "%"
    pressure = str(raw_weather_data["main"]["pressure"]) + " mb"
    icon = raw_weather_data["weather"][0]["icon"]

    wetdata = [
        name,
        weather_main,
        temperature,
        wind_speed,
        humidity,
        pressure,
        current_time,
        icon,
    ]
    return wetdata


@app.route("/weather/<postalcode>")
def index(postalcode):
    data = get_weather(postalcode)
    return render_template(
        "index.html",
        name=data[0],
        weather_main=data[1],
        temperature=data[2],
        wind_speed=data[3],
        humidity=data[4],
        pressure=data[5],
        time=data[6],
        icon=data[7],
    )


while True:
    app.run(host="127.0.0.1", port=8000, debug=True)
