"""
The goal of this project is to create a weather app that shows the current weather conditions
and forecast for a specific location.
"""

import sys
import requests
import tkinter as tki
from PIL import ImageTk, Image
from datetime import datetime


class WeatherApp:
    def __init__(self, weather_data):
        self._data = weather_data
        self._root = tki.Tk()
        self._root.geometry("225x225")

        self._weather_icon = None
        self._time_label = None

        self._create_name()
        self._create_time()
        self._create_temperature()
        self._create_icon_image()
        self._create_description()

        self._root.mainloop()

    def _create_name(self):
        city_name = self._data["name"]
        tki.Label(self._root, text=city_name).pack()

    def _create_icon_image(self):
        icon_url = f"http://openweathermap.org/img/w/{self._data['weather'][0]['icon']}.png"
        icon_response = requests.get(icon_url, stream=True)
        icon_image = Image.open(icon_response.raw)
        self._weather_icon = ImageTk.PhotoImage(icon_image)
        tki.Label(self._root, image=self._weather_icon).pack()

    def _create_time(self):
        self._time_label = tki.Label(self._root)
        self._time_label.pack()
        self._update_clock()

    def _update_clock(self):
        time = datetime.now().strftime("%m/%d/%Y, %H:%M")
        self._time_label.config(text=time)
        self._root.after(1000, self._update_clock)

    def _create_temperature(self):
        temp = f"{self._data['main']['temp']}°C"
        tki.Label(self._root, text=temp, font=("Arial", 32), fg="green").pack()

    def _create_description(self):
        desc = self._data['weather'][0]['description'].capitalize()
        tki.Label(self._root, text=desc).pack()


def get_weather_service(city, country):
    url = "http://api.openweathermap.org/data/2.5/weather"
    parameters = {'q': city + ',' + country, "appid": "482ba6eb027c01498e6f6e28129d924d",
                  "units": "metric"}
    r = requests.get(url, params=parameters)
    data = r.json()
    if r.status_code != 200:
        raise Exception()
    return data


def main():
    try:
        weather_data = get_weather_service(sys.argv[1], sys.argv[2])
        WeatherApp(weather_data)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
