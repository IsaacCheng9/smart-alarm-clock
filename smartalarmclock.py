"""
A smart alarm clock presented in a basic web interface, created using the
Flask module in Python. The user is able to read updated weather and news
information, and set alarms for the future.
"""

import json
import sched
from datetime import date, datetime, timedelta
from time import mktime, time

import pyttsx3
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def main():
    """
    Shows the current time, the latest news headlines, and a weather forecast
    summary.
    """

    current_datetime = last_updated()
    keys = parse_configs()
    forecast, temp, max_temp, min_temp, wind = get_weather(keys)
    (headline1, headline2, headline3, headline4, headline5, headline6,
     headline7, headline8, headline9, headline10) = get_news(keys)
    return render_template("home.html", current_datetime=current_datetime,
                           forecast=forecast, temp=temp,
                           max_temp=max_temp, min_temp=min_temp, wind=wind,
                           headline1=headline1, headline2=headline2,
                           headline3=headline3, headline4=headline4,
                           headline5=headline5, headline6=headline6,
                           headline7=headline7, headline8=headline8,
                           headline9=headline9, headline10=headline10)
    set_alarm_clock()


def last_updated():
    """
    Displays the date and time of last update.

    Returns:
        current_datetime (datetime): Displays the last time data was updated.
    """

    current_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    print("Last Updated:\n    ", current_datetime)

    return current_datetime


def parse_configs():
    """
    Gets the API keys from the JSON config file.

    Returns:
        api_keys (dict): Stores the API keys for weather and news data.
    """

    # Loads the config file and finds the API keys.
    with open("config.json", "r") as file:
        config = json.load(file)
    api_keys = config["api_keys"]

    return api_keys


def get_weather(api_keys: dict):
    """
    Gets the weather forecast summary.

    Args:
        api_keys (dict): Stores the API keys for weather and news data.

    Returns:
        forecast (str): Displays type of weather forecast.
        temp (str): Displays temperature for weather forecast.
        max_temp (str): Displays maximum temperature for weather forecast.
        min_temp (str): Displays minimum temperature for weather forecast.
        wind (str): Displays average wind speed for weather forecast.
    """

    # Gets the API for weather data on user's city.
    """weather_api = ("https://api.openweathermap.org/data/2.5/weather?"
                   "q={}&appid=8bb8c8c3507631f11bb9599e7795a718"
                   "&units=metric").format(city)"""
    weather_key = api_keys["weather"]
    weather_api = ("https://api.openweathermap.org/data/2.5/weather?"
                   "q=exeter&appid=8bb8c8c3507631f11bb9599e7795a718"
                   "&units=metric").format(weather_key)

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
          min_temp + "°C.\n    Wind speeds of", wind, "m/s.")

    return forecast, temp, max_temp, min_temp, wind


def get_news(api_keys: dict):
    """
    Gets the news headlines.

    Args:
        api_keys (dict): Stores the API keys for weather and news data.

    Returns:
        headline# (str): Stores the numbered headline (depending on #).
    """

    # Gets latest news using the news API.
    news_key = api_keys["news"]
    news_api = ("https://newsapi.org/v2/top-headlines?"
                "country=gb&apiKey={}").format(news_key)

    # Gets news using the news API.
    raw_news = requests.get(news_api)
    news = raw_news.json()

    # Gets and assigns top ten headlines.
    headline1 = str(news["articles"][0]["title"])
    headline2 = str(news["articles"][1]["title"])
    headline3 = str(news["articles"][2]["title"])
    headline4 = str(news["articles"][3]["title"])
    headline5 = str(news["articles"][4]["title"])
    headline6 = str(news["articles"][5]["title"])
    headline7 = str(news["articles"][6]["title"])
    headline8 = str(news["articles"][7]["title"])
    headline9 = str(news["articles"][8]["title"])
    headline10 = str(news["articles"][9]["title"])

    # Prints the top ten headlines.
    print("\nNews Headlines for Today:")
    for i in range(10):
        articles = str(news["articles"][i]["title"])
        print("    #:" + str(i + 1), articles)

    return (headline1, headline2, headline3, headline4, headline5, headline6,
            headline7, headline8, headline9, headline10)


def alert_alarm():
    """
    Alerts the user when their alarm is going off.
    """

    text_to_speech = pyttsx3.init()
    text_to_speech.say("Your alarm is going off!")
    print("\nYour alarm is going off!")
    text_to_speech.runAndWait()


def set_alarm_clock():
    """
    Asks the user if they want to set an alarm.
    """

    # Gets the alarm time from the new alarm input box and calculates delay.
    alarm_time = request.args.get("alarm")
    format_time = datetime.strptime(alarm_time, "%Y-%m-%dT%H:%M")
    alarm_time = mktime(alarm_time.timetuple())
    delay = alarm_time - time()

    # Activates new alarm.
    alarm = sched.scheduler(time.time)
    alarm.enter(delay, 1, alert_alarm)
    alarm.run()


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    app.run(debug=True)
