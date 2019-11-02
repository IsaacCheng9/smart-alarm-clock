"""
A smart alarm clock presented in a basic web interface.
"""

from collections import OrderedDict
from datetime import datetime
import json
import requests


def main():
    """
    Shows the current time, the latest news headlines, and a weather forecast
    summary.
    """

    show_time()
    show_weather()
    show_news()
    set_alarm_clock()


def show_time():
    """
    Displays the current date and time.
    """

    current_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    print("Current Date and Time:\n    ", current_datetime)


def show_weather():
    """
    Shows a weather forecast summary for the user's city.
    """

    # Gets the API for weather data on user's city.
    city = input("\nPlease enter your city. ").capitalize()
    weather_api = ("https://api.openweathermap.org/data/2.5/weather?"
                   "q={}&appid=8bb8c8c3507631f11bb9599e7795a718"
                   "&units=metric").format(city)

    # Gets weather data using the weather API.
    raw_weather = requests.get(weather_api)
    weather = raw_weather.json()
    forecast = weather["weather"][0]["main"]
    temp = str(weather["main"]["temp"])
    max_temp = str(weather["main"]["temp_max"])
    min_temp = str(weather["main"]["temp_min"])
    wind = str(weather["wind"]["speed"])

    # Prints a weather forecast summary.
    print("\nWeather Forecast:\n    " + forecast,
          "with an average temperature of", temp +
          "°C.\n    Temperature highs of", max_temp + "°C and lows of",
          min_temp + "°C.\n    Wind speeds of", wind, "km/h.")


def show_news():
    """
    Shows the world news headlines.
    """

    # Gets latest news using the news API.
    news_api = ("https://newsapi.org/v2/top-headlines?"
                "country=us&apiKey=86a97a39f14a4a1eac894868d7b9726c")

    # Gets news using the news API.
    raw_news = requests.get(news_api)
    news = raw_news.json()

    # Prints the top ten world news headlines.
    print("\nNews Headlines for Today:")
    for i in range(10):
        articles = str(news["articles"][i]["title"])
        print("    #" + str(i + 1), articles)


def set_alarm_clock():
    """
    Asks the user if they want to set an alarm.
    """

    set_alarm = input("\nWould you like to set a new alarm? (y/n) ").lower()
    if set_alarm == "y":
        alarm = input("What time would you like to set an alarm for? (HH:MM) ")


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
