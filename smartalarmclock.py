"""
A smart alarm clock presented in a basic web interface.
"""

from datetime import datetime
import json
import requests


def main():
    """
    Defines the weather and news APIs to get data from, and then runs the
    program.
    """
    weather_api = ("https://api.openweathermap.org/data/2.5/weather?"
                   "q=Exeter&appid=8bb8c8c3507631f11bb9599e7795a718")
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
    print("Current Date and Time:", current_datetime)


def show_news_weather(weather_api: str, news_api: str):
    """
    Shows the news and weather for the user's chosen city.

    Args:
        weather_api (str): The weather API URL from OpenWeatherMap.
        news_api (str): The news API URL from NewsAPI.
    """

    weather = requests.get(weather_api).json()
    print(json.dumps(weather, indent=4, sort_keys=True))

    news = requests.get(news_api).json()
    print(json.dumps(news, indent=4, sort_keys=True))


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
