"""
A smart alarm clock presented in a basic web interface, created using the
Flask module in Python. The user is able to read updated weather and news
information, receiving notifications if new weather or news information is
obtained. The user can also set alarms for the future (including alarms which
repeat every day), and cancel these alarms if they change their mind.
"""

import json
import logging
import sched
from datetime import datetime
from time import localtime, mktime, sleep, strftime, strptime, time

import pyttsx3
import requests
from flask import Flask, render_template, request

upcoming_alarms = []
news_notifications = []
weather_notifications = []
old_headlines = []
old_forecast = ""
old_temp = ""

# Initialises Flask for web interface and the scheduler for the alarm.
app = Flask(__name__)
alarm = sched.scheduler(time, sleep)


@app.route("/")
def main() -> str:
    """
    Shows the current time, the latest news headlines, and a weather forecast
    summary.

    Returns:
        render_template() (str): Renders the HTML to display on webpage.
    """

    # Sets up the API keys and file paths, then starts logging.
    api_keys, file_paths, location = parse_configs()
    setup_logging(file_paths)

    # Updates weather and news, and shows the last updated time.
    current_datetime = last_updated()
    forecast, temp, max_temp, min_temp, wind = get_weather(api_keys, location)
    headlines = get_news(api_keys, location)

    # Checks for alarm inputs.
    get_alarm_inputs()

    # Returns the variables to the HTML file to render webpage.
    return render_template("home.html", current_datetime=current_datetime,
                           weather_notifications=weather_notifications,
                           news_notifications=news_notifications,
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


def get_notifications(notification_type: str, new_notification: str) -> list:
    """
    Adds notifications as news, weather, or alarms are changed.

    Args:
        notification_type (str): Stores the type of notification for
                                 categorisation.
        new_notification (str): Stores the new notification to be added.

    Returns:
        news_notifications (list): Stores a list of news notifications to be
                                   displayed.
        weather_notifications (list): Stores a list of weather notifications to
                                      be displayed.
    """

    # Adds a timestamp to new notifications.
    notification_input = (datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "
                          + new_notification)

    # Adds notification to the relevant notification category list.
    if notification_type == "News":
        news_notifications.insert(0, notification_input)
    elif notification_type == "Weather":
        weather_notifications.insert(0, notification_input)

    return news_notifications, weather_notifications


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

    global old_forecast, old_temp

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

    # Adds notification if forecast or temperature changes, stating the change.
    if forecast != old_forecast:
        new_forecast = (
            "The weather forecast has changed. It is now " + forecast.lower()
            + ".")
        get_notifications("Weather", new_forecast)
    if temp != old_temp:
        new_temp = ("The current temperature has changed. It is now " +
                    temp + "°C.")
        get_notifications("Weather", new_temp)

    # Sets forecast and temperature as old values to check for changes.
    old_forecast = forecast
    old_temp = temp

    return forecast, temp, max_temp, min_temp, wind


def get_news(api_keys: dict, location: dict) -> list:
    """
    Gets the news headlines.

    Args:
        api_keys (dict): Stores the API keys for weather and news data.
        location (dict): Stores the location to enable local news and weather.

    Returns:
        headlines (list): Stores the list of headlines to be displayed.
    """

    global old_headlines

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

    # Adds notification that news was updated, specifying the new headline.
    for headline in headlines:
        if headline not in old_headlines:
            new_headline = ("A new headline has been added: " + headline)
            get_notifications("News", new_headline)

    # Adds the headlines to the old headlines list to check for new headlines.
    old_headlines = headlines

    return headlines


def get_alarm_inputs():
    """
    Gets the alarm inputs from the forms in the webpage.
    """

    # Gets the alarm time from the new alarm input box and calculates delay.
    alarm_time = request.args.get("alarm")
    alarm_label = request.args.get("alarm_label")
    alarm_repeat = request.args.get("alarm_repeat")
    alarm.run(blocking=False)

    # Gets the time for the alarm to cancel.
    alarm_cancel = request.args.get("cancel_alarm")

    # Checks if the user has input an alarm to set.
    if alarm_time:
        # Converts from input box time format to epoch time format.
        format_time = strptime(alarm_time, "%Y-%m-%dT%H:%M")
        format_time = mktime(format_time)

        # Schedules the alarm if there's an alarm input.
        set_alarm(alarm_time, alarm_label, alarm_repeat, format_time)

    # Checks if the user has input an alarm to cancel.
    if alarm_cancel:
        cancel_alarm(alarm_cancel)


def set_alarm(alarm_time: str, alarm_label: str, alarm_repeat: str,
              format_time: float) -> list:
    """
    Sets a new alarm according to the inputs of the user.

    Args:
        alarm_time (str): The date and time of the alarm.
        alarm_label (str): The label of the alarm.
        alarm_repeat (str): Whether the alarm repeats or not.
        format_time (float): The alarm input in epoch time.

    Returns:
        upcoming_alarms (list): A list of the upcoming alarms.
    """

    global upcoming_alarms

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


def alert_alarm(alarm_time: str, alarm_label: str, alarm_repeat: str) -> list:
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

    # Deletes the alarm from the alarms list.
    del upcoming_alarms[0]

    # Repeats the alarm for the next day if repeating alarm option is set.
    if alarm_repeat:
        # Converts alarm time to epoch time and adds an extra day.
        format_time = strptime(alarm_time, "%Y-%m-%dT%H:%M")
        format_time = mktime(format_time)
        format_time += 86400

        # Converts back from epoch time to datetime.
        alarm_time = strftime("%Y-%m-%dT%H:%M", localtime(format_time))

        # Sets the alarm for the same time the next day.
        set_alarm(alarm_time, alarm_label, alarm_repeat, format_time)

    return upcoming_alarms


def cancel_alarm(alarm_cancel: str):
    """
    Allows the user to cancel an alarm.

    Args:
        alarm_cancel (str): The alarm which the user wants to cancel.
    """

    # Cancels the inputted alarm from the queue and removes it from list.
    alarm_cancel_epoch = strptime(alarm_cancel, "%Y-%m-%dT%H:%M")
    alarm_cancel_epoch = mktime(alarm_cancel_epoch)
    for event in alarm.queue:
        epoch = event[0]
        if epoch == alarm_cancel_epoch:
            index = alarm.queue.index(event)
            del upcoming_alarms[index]
            alarm.cancel(event)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    app.run(debug=True)
