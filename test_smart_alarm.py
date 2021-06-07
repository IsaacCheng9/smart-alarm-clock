import unittest

from smart_alarm import cancel_alarm, get_news, last_updated, parse_configs, set_alarm


class TestParseConfigs(unittest.TestCase):
    # Checks if the config file output is a tuple of dictionaries.
    def test_config_file(self):
        self.assertIsInstance(parse_configs(), tuple)


class TestLastUpdated(unittest.TestCase):
    # Checks if current_datetime is a string variable.
    def test_current_datetime_type(self):
        self.assertIsInstance(last_updated(), str)


"""class TestGetNotifications(unittest.TestCase):
    # Checks if news_notifications is a list variable.
    def test_datetime_type(self):
        self.assertIsInstance(get_news(api_keys, location), list)


class TestGetNews(unittest.TestCase):
    # Raises error if two lists aren't equal.
    def test_news_headlines(self):
        self.assertListNotEqual(get_news(api_keys, location).old_headlines, get_news(
            api_keys, location).headlines)


class TestGetAlarmInputs(unittest.TestCase):
    # Passes if a ValueError is raised with input of 'x'.

    def test_alarm_values(self):
        self.assertRaises(ValueError, get_alarms().alarm_time, "x")


class TestSetAlarm(unittest.TestCase):
    # Checks if upcoming_alarms is a list variable.
    def test_datetime_type(self):
        self.assertIsInstance(set_alarm(
            alarm_time, alarm_label, alarm_repeat, format_time).upcoming_alarms, list)


class TestCancelAlarm(unittest.TestCase):
    # Passes if a ValueError is raised with input of 'x'.
    def test_cancel_alarm_values(self):
        self.assertRaises(ValueError, cancel_alarm("x").alarm_time)"""


if __name__ == "__main__":
    unittest.main()
