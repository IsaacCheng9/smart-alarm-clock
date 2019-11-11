"""
A smart alarm clock presented in a basic web interface, created using the
Flask module in Python. The user is able to read updated weather and news
information, and set alarms for the future.
"""

import sched
from datetime import date, datetime, timedelta
import time

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
    # current_alarms = set_alarm()
    set_alarm()
    return render_template("alarm_home.html",
                           current_datetime=current_datetime)


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


def alert_alarm():
    """
    Alerts the user when their alarm is going off.
    """

    # text_to_speech = pyttsx3.init()
    # text_to_speech.say("Your alarm is going off!")
    # text_to_speech.runAndWait()
    print("\nYour alarm is going off!")


# @app.route("/setalarm")
def set_alarm():
    """
    Allows the user to set an alarm.
    """

    # current_alarms = []

    # Gets the alarm time from the new alarm input box and calculates delay.
    alarm_time = request.args.get("alarm")

    if alarm_time:
        print(alarm_time)
        format_time = time.strptime(alarm_time, "%Y-%m-%dT%H:%M")
        # format_time = mktime(alarm_time.timetuple()
        format_time = time.mktime(format_time)
        # delay = alarm_time - time()

        # Activates new alarm.
        alarm = sched.scheduler(time.time, time.sleep)
        # alarm.enter(delay, 1, alert_alarm)
        alarm.enterabs(format_time, 1, alert_alarm)
        alarm.run()

        # current_alarms.append(format_time)

    # current_alarms = str(current_alarms)

    # return current_alarms
    # return render_template("set_alarm.html")


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    app.run(debug=True)
