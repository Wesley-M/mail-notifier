import unittest
import tempfile
import os
from unittest.mock import patch
import numpy as np

from main import *

MAIL_FORMAT = {
    "ACCOUNT_EMAIL": 0,
    "SENDER_EMAIL": 1,
    "SUBJECT": 2
}


class TestMain(unittest.TestCase):
    def test_check_valid_installation(self):
        # The script was not installed yet.
        with self.assertRaises(SystemExit) as cm:
            check_if_valid_installation("/nonexistent/path")
        self.assertEqual(cm.exception.code, 1)

        # The config file was not found :( The installation might have failed.
        with self.assertRaises(SystemExit) as cm:
            check_if_valid_installation("/var")
        self.assertEqual(cm.exception.code, 1)

    def test_read_config(self):
        # Create temporary config file
        with tempfile.TemporaryDirectory() as tempdir:
            tmpfilepath = os.path.join(tempdir, 'config.json')
            with open(tmpfilepath, 'w') as tmpfile:
                tmpfile.write("""
                    {
                        "search_for": [
                            {
                                "name": "Linx",
                                "sender": ".*linx.*",
                                "subject": ".*linx.*"
                            }
                        ],
                        "inspect_x_last_emails": 10
                    }
                """)

            config = read_config(tempdir)
            self.assertEqual(config["search_for"][0]["name"], "Linx")
            self.assertEqual(config["search_for"][0]["sender"], ".*linx.*")
            self.assertEqual(config["search_for"][0]["subject"], ".*linx.*")
            self.assertEqual(config["inspect_x_last_emails"], 10)

    def test_get_new_emails(self):
        global MAIL_FORMAT

        testargs = [
            "job-notifier",
            "2",
            "wesleymatteus99@gmail.com (Gmail)",
            "support@turing.com",
            "Hey Wesley, update your availability before it expires.",
            "wesleymatteus99@gmail.com (Gmail)",
            "team@email.researcher-app.com",
            "Hi Wesley Matteus, don’t miss out on your top papers this week"
        ]

        with patch.object(sys, 'argv', testargs):
            np.testing.assert_array_equal(get_new_emails(MAIL_FORMAT), [
                ['wesleymatteus99@gmail.com (Gmail)', 'support@turing.com', 'Hey Wesley, update your availability before it expires.'],
                ['wesleymatteus99@gmail.com (Gmail)', 'team@email.researcher-app.com', 'Hi Wesley Matteus, don’t miss out on your top papers this week']
            ])

    def test_get_notifications_by_sender_pattern(self):
        global MAIL_FORMAT

        emails = [
            ['wesleymatteus99@gmail.com (Gmail)', 'support@turing.com', 'Hey Wesley, update your availability before it expires.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'jobs-listings@linkedin.com', 'Unimed Grande Florianópolis está contratando.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'team@email.researcher-app.com', 'Hi Wesley Matteus, don’t miss out on your top papers this week']
        ]

        search_for = [
            {
                "name": "Linkedin",
                "sender": ".*linkedin.*"
            }
        ]

        inspect_x_last_emails = 10

        notifications = get_notifications(emails, MAIL_FORMAT, search_for, inspect_x_last_emails)
        
        np.testing.assert_array_equal(notifications, [
            ['Pattern: Linkedin', 'Sender: jobs-listings@linkedin.com \n\nUnimed Grande Florianópolis está contratando.']
        ])
    
    def test_get_notifications_by_subject_pattern(self):
        global MAIL_FORMAT

        emails = [
            ['wesleymatteus99@gmail.com (Gmail)', 'support@turing.com', 'Hey Wesley, update your availability before it expires.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'jobs-listings@linkedin.com', 'Unimed Grande Florianópolis está contratando.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'team@email.researcher-app.com', 'Hi Wesley Matteus, don’t miss out on your top papers this week']
        ]

        search_for = [
            {
                "name": "Wesley",
                "subject": ".*wesley.*"
            }
        ]

        inspect_x_last_emails = 10

        notifications = get_notifications(emails, MAIL_FORMAT, search_for, inspect_x_last_emails)
        
        np.testing.assert_array_equal(notifications, [
            ['Pattern: Wesley', 'Sender: support@turing.com \n\nHey Wesley, update your availability before it expires.'],
            ['Pattern: Wesley', 'Sender: team@email.researcher-app.com \n\nHi Wesley Matteus, don’t miss out on your top papers this week']
        ])

    def test_get_notifications_by_sender_and_subject_pattern(self):
        global MAIL_FORMAT

        emails = [
            ['wesleymatteus99@gmail.com (Gmail)', 'support@turing.com', 'Hey Wesley, update your availability before it expires.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'jobs-listings@linkedin.com', 'Unimed Grande Florianópolis está contratando.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'jobs-listings@linkedin.com', 'Generic message.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'team@email.researcher-app.com', 'Hi Wesley Matteus, don’t miss out on your top papers this week']
        ]

        search_for = [
            {
                "name": "Linkedin AND Unimed",
                "subject": ".*unimed.*",
                "sender": ".*linkedin.*"
            }
        ]

        inspect_x_last_emails = 10

        notifications = get_notifications(emails, MAIL_FORMAT, search_for, inspect_x_last_emails)
        
        np.testing.assert_array_equal(notifications, [
            ['Pattern: Linkedin AND Unimed', 'Sender: jobs-listings@linkedin.com \n\nUnimed Grande Florianópolis está contratando.']
        ])

    def test_get_notifications_by_sender_or_subject_pattern_with_restrictions(self):
        global MAIL_FORMAT

        emails = [
            ['wesleymatteus99@gmail.com (Gmail)', 'support@turing.com', 'Hey Wesley, update your availability before it expires.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'jobs-listings@linkedin.com', 'Unimed Grande Florianópolis está contratando.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'team@email.researcher-app.com', 'Hi Wesley Matteus, don’t miss out on your top papers this week']
        ]

        search_for = [
            {
                "name": "Linkedin AND Unimed",
                "subject": ".*unimed.*",
                "sender": ".*linkedin.*"
            }
        ]

        inspect_x_last_emails = 10

        notifications = get_notifications(emails, MAIL_FORMAT, search_for, inspect_x_last_emails)
        
        np.testing.assert_array_equal(notifications, [
            ['Pattern: Linkedin AND Unimed', 'Sender: jobs-listings@linkedin.com \n\nUnimed Grande Florianópolis está contratando.']
        ])

    def test_get_notifications_limiting_inspection_range(self):
        global MAIL_FORMAT

        emails = [
            ['wesleymatteus99@gmail.com (Gmail)', 'support@turing.com', 'Hey Wesley, update your availability before it expires.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'jobs-listings@linkedin.com', 'Unimed Grande Florianópolis está contratando.'],
            ['wesleymatteus99@gmail.com (Gmail)', 'team@email.researcher-app.com', 'Hi Wesley Matteus, don’t miss out on your top papers this week']
        ]

        search_for = [
            {
                "name": "Unimed",
                "subject": ".*unimed.*",
            }
        ]

        inspect_x_last_emails = 1
        notifications = get_notifications(emails, MAIL_FORMAT, search_for, inspect_x_last_emails)
        np.testing.assert_array_equal(notifications, [])

        inspect_x_last_emails = 2
        notifications = get_notifications(emails, MAIL_FORMAT, search_for, inspect_x_last_emails)
        np.testing.assert_array_equal(notifications, [
            ['Pattern: Unimed', 'Sender: jobs-listings@linkedin.com \n\nUnimed Grande Florianópolis está contratando.']
        ])