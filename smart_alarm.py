"""
A smart alarm clock presented in a basic web interface, created using the
Flask module in Python. The user is able to read updated weather and news
information, and set alarms for the future.
"""

import json
import logging
import sched
import time
from datetime import datetime

import pyttsx3
import requests
from flask import Flask, render_template, request

notifications = []
notification1 = ""
notification2 = ""
notification3 = ""
notification4 = ""
notification5 = ""

upcoming_alarms = []
upcoming_alarms_labels = []
display_alarms = ""

# Initialises Flask for web interface and the scheduler for the alarm.
app = Flask(__name__)
alarm = sched.scheduler(time.time, time.sleep)


@app.route("/")
def main():
    """
    Shows the current time, the latest news headlines, and a weather forecast
    summary.
    """

    # Sets up the API keys and file paths, then starts logging.
    api_keys, file_paths = parse_configs()
    setup_logging(file_paths)

    # Updates weather and news, and shows the last updated time.
    current_datetime = last_updated()
    forecast, temp, max_temp, min_temp, wind = get_weather(api_keys)
    (headline1, headline2, headline3, headline4, headline5, headline6,
     headline7, headline8, headline9, headline10) = get_news(api_keys)

    # Enables alarm functionality.
    alarm_time, alarm_label, alarm_repeat, format_time = get_alarm()
    upcoming_alarms, displayed_alarms = set_alarm(alarm_time, alarm_label,
                                                  alarm_repeat, format_time)
    cancel_alarm()

    # Returns the variables to the HTML file to render webpage.
    return render_template("home.html", current_datetime=current_datetime,
                           notification1=notification1,
                           notification2=notification2,
                           notification3=notification3,
                           notification4=notification4,
                           notification5=notification5,
                           forecast=forecast, temp=temp,
                           max_temp=max_temp, min_temp=min_temp, wind=wind,
                           headline1=headline1, headline2=headline2,
                           headline3=headline3, headline4=headline4,
                           headline5=headline5, headline6=headline6,
                           headline7=headline7, headline8=headline8,
                           headline9=headline9, headline10=headline10,
                           displayed_alarms=displayed_alarms)


def parse_configs() -> dict:
    """
    Gets the API keys from the JSON config file.

    Returns:
        api_keys (dict): Stores the API keys for weather and news data.
        file_paths (dict): Stores the file path for logging.
    """

    # Loads the config file and finds the API keys.
    with open("config.json", "r") as file:
        config = json.load(file)
    api_keys = config["api_keys"]
    file_paths = config["file_paths"]

    return api_keys, file_paths


def setup_logging(file_paths: dict):
    """
    Sets up the logging system to automatically log actions performed in the
    program.

    Args:
        file_paths (dict): Stores the file path for logging.
    """

    log_file = file_paths["logging"]

    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Smart alarm clock started.")


def last_updated() -> datetime:
    """
    Displays the date and time of last update.

    Returns:
        current_datetime (datetime): Displays the last time data was updated.
    """

    current_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    print("Last Updated:\n    ", current_datetime)

    return current_datetime


def get_notifications(new_notification: str):
    """
    Adds notifications as news, weather, or alarms are changed.

    Args:
        new_notification (str): Stores the new notification to be added.

    Returns:
        notifications# (str): Stores the numbered notification (depending on
                              #).
    """

    global notification1, notification2, notification3, notification4
    global notification5

    # Adds new notification to the list.
    notifications.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "
                         + new_notification)

    # Gets the latest five notifications.
    try:
        notification1 = notifications[-1]
        notification2 = notifications[-2]
        notification3 = notifications[-3]
        notification4 = notifications[-4]
        notification5 = notifications[-5]
    # Prevents crashing when there are no notifications on program startup.
    except IndexError:
        pass

    return (notification1, notification2, notification3, notification4,
            notification5)


def get_weather(api_keys: dict) -> str:
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

    get_notifications("Weather has been updated.")

    return forecast, temp, max_temp, min_temp, wind


def get_news(api_keys: dict) -> str:
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

    get_notifications("News headlines have been updated.")

    return (headline1, headline2, headline3, headline4, headline5, headline6,
            headline7, headline8, headline9, headline10)


def alert_alarm(alarm_time: str, alarm_label: str, alarm_repeat: str):
    """
    Alerts the user when their alarm is going off.

    Args:
        alarm_label (str): The label associated with the alarm.
    """

    # Alert user about their alarm via voiceover.
    text_to_speech = pyttsx3.init()
    text_to_speech.say(("Your alarm label", alarm_label, "is going off."))
    text_to_speech.runAndWait()

    # Alert user about their alarm via notifications.
    print("\nYour alarm with label", alarm_label, "is going off!")
    get_notifications("Alarm with label", alarm_label, "is going off!")

    if alarm_repeat:
        """new_date = int(alarm_time[8:10]) + 1
        alarm_time = alarm_time[:8] + str(new_date) + alarm_time[10:]
        set_alarm(alarm_time, alarm_label, alarm_repeat)"""

        set_alarm(alarm_time, alarm_label, alarm_repeat, format_time)

        # return alarm_time, alarm_label, alarm_repeat


def get_alarm() -> str:
    """
    Gets new alarm input from web form.

    Returns:
        alarm_time (str): The date and time of the alarm.
        alarm_label (str): The label of the alarm.
        alarm_repeat (str): Whether the alarm repeats or not.
        format_time (float): Enoch time formatted version of alarm_time.
    """

    # Gets the alarm time from the new alarm input box and calculates delay.
    alarm_time = request.args.get("alarm")
    alarm_label = request.args.get("alarm_label")
    alarm_repeat = request.args.get("alarm_repeat")
    alarm.run(blocking=False)

    # Converts from input box time format to epoch time format.
    if alarm_time:
        format_time = time.strptime(alarm_time, "%Y-%m-%dT%H:%M")
        format_time = time.mktime(format_time)

    return alarm_time, alarm_label, alarm_repeat, format_time


def set_alarm(alarm_time: str, alarm_label: str, alarm_repeat: str,
              format_time: float) -> list:
    """
    Allows the user to set an alarm.

    Args:
        alarm_time (str): The date and time of the alarm.
        alarm_label (str): The label of the alarm.
        alarm_repeat (str): Whether the alarm repeats or not.

    Returns:
        upcoming_alarms (list): A list of the upcoming alarms.
        displayed_alarms (str): A string list of the upcoming alarms.
    """

    global upcoming_alarms, upcoming_alarms_labels
    displayed_alarms = ""

    # Activates new alarm to alert at given time.
    alarm.enterabs(format_time, 1, alert_alarm, argument=(alarm_time,
                                                          alarm_label,
                                                          alarm_repeat,))

    # Combines the alarm time and the alarm label for display in webpage.
    if alarm_repeat:
        alarm_input = (alarm_time.replace("T", " ") + " " + alarm_label +
                       " (" + alarm_repeat + ")")
    else:
        alarm_input = (alarm_time.replace("T", " ") + " " + alarm_label)

    # Adds alarm to the list of alarms and sorts them chronologically.
    upcoming_alarms.append(alarm_input)
    upcoming_alarms = sorted(upcoming_alarms)

    # Creates the displayed list of alarms.
    for alarm_input in upcoming_alarms:
        if alarm_input not in displayed_alarms:
            displayed_alarms += "\n" + alarm_input

    # get_notifications("A new alarm has been added.")

    return upcoming_alarms, displayed_alarms


def cancel_alarm():
    """
    Allows the user to cancel an alarm.
    Args:
        upcoming_alarms (str): A list of the upcoming alarms.
    """

    alarm_cancel = request.args.get("cancel_alarm")

    # Looks for the inputted alarm and cancels it.
    if alarm_cancel:
        alarm_cancel_epoch = time.strptime(alarm_cancel, "%Y-%m-%dT%H:%M")
        alarm_cancel_epoch = time.mktime(alarm_cancel_epoch)
        for event in alarm.queue:
            epoch = event[0]
            if epoch == alarm_cancel_epoch:
                alarm.cancel(event)
                get_notifications(
                    "Your alarm has successfully been cancelled.")


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    app.run(debug=True)
