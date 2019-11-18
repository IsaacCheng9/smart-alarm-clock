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

upcoming_alarms = []
notifications = []

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
    api_keys, file_paths, location = parse_configs()
    setup_logging(file_paths)

    # Updates weather and news, and shows the last updated time.
    current_datetime = last_updated()
    forecast, temp, max_temp, min_temp, wind = get_weather(api_keys, location)
    headlines = get_news(api_keys, location)

    # Enables alarm functionality.
    upcoming_alarms = set_alarm()
    cancel_alarm()

    # Returns the variables to the HTML file to render webpage.
    return render_template("home.html", current_datetime=current_datetime,
                           notifications=notifications,
                           forecast=forecast, temp=temp,
                           max_temp=max_temp, min_temp=min_temp, wind=wind,
                           headlines=headlines,
                           upcoming_alarms=upcoming_alarms)


def parse_configs() -> dict:
    """
    Gets the API keys from the JSON config file.

    Returns:
        api_keys (dict): Stores the API keys for weather and news data.
        file_paths (dict): Stores the file path for logging.
        location (dict): Stores the location to enable local news and weather.
    """

    # Loads the config file and finds the API keys.
    with open("config.json", "r") as file:
        config = json.load(file)
    api_keys = config["api_keys"]
    file_paths = config["file_paths"]
    location = config["location"]

    return api_keys, file_paths, location


def setup_logging(file_paths: dict):
    """
    Sets up the logging system to automatically log actions performed in the
    program.

    Args:
        file_paths (dict): Stores the file path for logging.
    """

    # Gets the log file from the configuration file.
    log_file = file_paths["logging"]

    # Starts the logging system.
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Smart alarm clock started.")


def last_updated() -> datetime:
    """
    Displays the date and time of last update.

    Returns:
        current_datetime (datetime): Displays the last time data was updated.
    """

    # Gets the current datetime to show when the webpage was last updated.
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
        notifications (list): Stores a list of notifications to be displayed.
    """

    # Adds a new notification to the notification list with a timestamp.
    notification_input = (datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "
                          + new_notification)
    notifications.insert(0, notification_input)

    return notifications


def get_weather(api_keys: dict, location: dict) -> str:
    """
    Gets the weather forecast summary.

    Args:
        api_keys (dict): Stores the API keys for weather and news data.
        location (dict): Stores the location to enable local news and weather.

    Returns:
        forecast (str): Displays type of weather forecast.
        temp (str): Displays temperature for weather forecast.
        max_temp (str): Displays maximum temperature for weather forecast.
        min_temp (str): Displays minimum temperature for weather forecast.
        wind (str): Displays average wind speed for weather forecast.
    """

    # Gets the API for weather data on user's city.
    weather_key = api_keys["weather"]
    city = location["city"]
    weather_api = ("https://api.openweathermap.org/data/2.5/weather?"
                   "q={}&appid={}&units=metric").format(city, weather_key)

    # Gets weather data using the weather API.
    raw_weather = requests.get(weather_api)
    weather = raw_weather.json()
    forecast = weather["weather"][0]["main"]
    temp = str(weather["main"]["temp"])
    max_temp = str(weather["main"]["temp_max"])
    min_temp = str(weather["main"]["temp_min"])
    wind = str(weather["wind"]["speed"])

    # Adds notification that weather was updated.
    get_notifications("Weather has been updated.")

    return forecast, temp, max_temp, min_temp, wind


def get_news(api_keys: dict, location: dict) -> str:
    """
    Gets the news headlines.

    Args:
        api_keys (dict): Stores the API keys for weather and news data.
        location (dict): Stores the location to enable local news and weather.

    Returns:
        headlines (list): Stores the list of headlines to be displayed.
    """

    # Declares list of headlines to be displayed.
    headlines = []

    # Gets latest news using the news API.
    news_key = api_keys["news"]
    country = location["country"]
    news_api = ("https://newsapi.org/v2/top-headlines?"
                "country={}&apiKey={}").format(country, news_key)

    # Gets news using the news API.
    raw_news = requests.get(news_api)
    news = raw_news.json()

    # Gets and appends top ten headlines to the list of headlines.
    for i in range(10):
        headline = "#" + str(i + 1) + ": " + str(news["articles"][i]["title"])
        headlines.append(headline)

    # Adds notification that news was updated.
    get_notifications("News has been updated.")

    return headlines


def alert_alarm(alarm_time: str, alarm_label: str, alarm_repeat: str):
    """
    Alerts the user when their alarm is going off.

    Args:
        alarm_time (str): The date and time of the alarm.
        alarm_label (str): The label of the alarm.
        alarm_repeat (str): Whether the alarm repeats or not.

    Returns:
        upcoming_alarms (list): A list of the upcoming alarms.
    """

    global upcoming_alarms

    # Alerts user about their alarm via voiceover.
    text_to_speech = pyttsx3.init()
    text_to_speech.say(("Your alarm with label", alarm_label, "is going off."))
    text_to_speech.runAndWait()

    # Prints when alarm is going off in console for debugging purposes.
    print("\nYour alarm with label", alarm_label, "is going off!")

    upcoming_alarms.pop(0)

    if alarm_repeat:
        format_time = time.strptime(alarm_time, "%Y-%m-%dT%H:%M")
        format_time = time.mktime(format_time)
        format_time += 30

        # Activates new alarm to alert at given time.
        alarm.enterabs(format_time, 1, alert_alarm, argument=(alarm_time,
                                                              alarm_label,
                                                              alarm_repeat))

        # Combines the alarm time and the alarm label for display.
        alarm_input = (alarm_time.replace("T", " ") + " " + alarm_label +
                       " (" + alarm_repeat + ")")

        # Adds alarm to the list of alarms and sorts them chronologically.
        upcoming_alarms.append(alarm_input)
        upcoming_alarms = sorted(upcoming_alarms)

    return upcoming_alarms


def set_alarm() -> list:
    """
    Allows the user to set an alarm.

    Returns:
        upcoming_alarms (list): A list of the upcoming alarms.
    """

    global upcoming_alarms
    displayed_alarms = ""

    # Gets the alarm time from the new alarm input box and calculates delay.
    alarm_time = request.args.get("alarm")
    alarm_label = request.args.get("alarm_label")
    alarm_repeat = request.args.get("alarm_repeat")
    alarm.run(blocking=False)

    # Converts from input box time format to epoch time format.
    if alarm_time:
        format_time = time.strptime(alarm_time, "%Y-%m-%dT%H:%M")
        format_time = time.mktime(format_time)

        # Activates new alarm to alert at given time.
        alarm.enterabs(format_time, 1, alert_alarm, argument=(alarm_time,
                                                              alarm_label,
                                                              alarm_repeat,))

        # Combines the alarm time and the alarm label for display.
        if alarm_repeat:
            alarm_input = (alarm_time.replace("T", " ") + " " + alarm_label +
                           " (" + alarm_repeat + ")")
        else:
            alarm_input = (alarm_time.replace("T", " ") + " " + alarm_label)

        # Adds alarm to the list of alarms and sorts them chronologically.
        upcoming_alarms.append(alarm_input)
        upcoming_alarms = sorted(upcoming_alarms)

    return upcoming_alarms


def cancel_alarm():
    """
    Allows the user to cancel an alarm.

    Args:
        upcoming_alarms (list): A list of the upcoming alarms.
    """

    # Gets the time for the alarm to cancel.
    alarm_cancel = request.args.get("cancel_alarm")

    # Cancels the inputted alarm from the queue and removes it from list.
    if alarm_cancel:
        alarm_cancel_epoch = time.strptime(alarm_cancel, "%Y-%m-%dT%H:%M")
        alarm_cancel_epoch = time.mktime(alarm_cancel_epoch)
        for event in alarm.queue:
            epoch = event[0]
            if epoch == alarm_cancel_epoch:
                index = alarm.queue.index(event)
                del upcoming_alarms[index]
                alarm.cancel(event)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    app.run(debug=True)
