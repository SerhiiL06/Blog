import requests


BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

API_KEY = open("weather/key.txt", "r").read()


def get_weather(city="Kyiv"):
    response = f"{BASE_URL}q={city}&appid={API_KEY}"
    check = requests.get(response).json()
    return {
        "temp": int(check["main"]["temp"] - 273.15),
        "description": check["weather"][0]["description"],
    }
