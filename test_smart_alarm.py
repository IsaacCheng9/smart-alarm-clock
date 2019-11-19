import unittest
import smart_alarm


class TestParseConfigs(unittest.TestCase):
    # Returns True if file is lowercase, else returns False.
    def test_file_capitalisation(self):
        self.assertTrue(smart_alarm.file.islower())
        self.assertFalse(smart_alarm.file.islower())


class TestLastUpdated(unittest.TestCase):
    # Checks if current_datetime is a datetime variable.
    def test_datetime_type(self):
        self.assertIsInstance(smart_alarm.current_datetime, datetime)


class TestGetNotifications(unittest.TestCase):
    # Checks if news_notifications is a list variable.
    def test_datetime_type(self):
        self.assertIsInstance(smart_alarm.news_notifications, list)


class TestGetNews(unittest.TestCase):
    # Raises error if two lists aren't equal.
    def test_news_headlines(self):
        self.assertListEqual(smart_alarm.old_headlines, smart_alarm.headlines)


class TestGetAlarmInputs(unittest.TestCase):
    # Passes if a ValueError is raised with input of 'x'.
    def test_values(self):
        self.assertRaises(ValueError, smart_alarm.alarm_time, "x")


class TestSetAlarm(unittest.TestCase):
    # Checks if upcoming_alarms is a list variable.
    def test_datetime_type(self):
        self.assertIsInstance(smart_alarm.upcoming_alarms, list)


if __name__ == "__main__":
    unittest.main()
