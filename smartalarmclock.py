"""
A smart alarm clock presented in a basic web interface.
"""

from collections import OrderedDict
from datetime import datetime
import json
import requests


def main():
    """
    Defines the weather and news APIs to get data from, and then runs the
    program.
    """
    weather_api = ("https://api.openweathermap.org/data/2.5/weather?"
                   "q=Exeter&units=metric&"
                   "appid=8bb8c8c3507631f11bb9599e7795a718")
    news_api = ("https://newsapi.org/v2/top-headlines?"
                "country=us&apiKey=86a97a39f14a4a1eac894868d7b9726c")

    show_time()
    show_news_weather(weather_api, news_api)


def show_time():
    """
    Displays the current date and time.
    """

    current_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    print("Current Date and Time:\n    ", current_datetime)


def show_news_weather(weather_api: str, news_api: str):
    """
    Shows the news and weather for the user's chosen city.

    Args:
        weather_api (str): The weather API URL from OpenWeatherMap.
        news_api (str): The news API URL from NewsAPI.
    """

    # Gets weather data using the weather API.
    raw_weather = requests.get(weather_api)
    weather = raw_weather.json()
    # print(json.dumps(weather, indent=4, sort_keys=True))
    forecast = weather["weather"][0]["main"]
    temp = str(weather["main"]["temp"])
    max_temp = str(weather["main"]["temp_max"])
    min_temp = str(weather["main"]["temp_min"])
    wind = str(weather["wind"]["speed"])

    # Gets news using the news API.
    raw_news = requests.get(news_api)
    news = raw_news.json()
    # print(json.dumps(news, indent=4, sort_keys=True))

    # Prints the ten news headlines.
    print("\nNews Headlines for Today:")
    for i in range(10):
        articles = str(news["articles"][i]["title"])
        print("    #" + str(i + 1), articles)

    # Prints a weather forecast summary.
    print("\nWeather Forecast:\n    " + forecast,
          "with an average temperature of", temp +
          "°C.\n    Temperature highs of", max_temp + "°C and lows of",
          min_temp + "°C.\n    Wind speeds of", wind, "km/h.")


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
