#!/usr/bin/env python3

import sys
import numpy as np
import json
import re
from os.path import exists
import subprocess

# -------------------
# 0. Check if script was installed and config file exists


def check_if_valid_installation(root):
    if (not exists(root)):
        print("The script was not installed yet.")
        sys.exit(1)

    if (not exists("{}/config.json".format(root))):
        print("The config file was not found :( The installation might have failed.")
        sys.exit(1)

# -------------------
# 1. Read config file


def read_config(root):
    """ Returns the config file as a dictionary """

    with open("{}/config.json".format(root)) as f:
        config = json.load(f)

    return config

# -------------------
# 2. Read new emails


def get_new_emails(mail_format):
    # New emails received (flat)
    emails_flat = sys.argv[2:]

    # New emails received (2D)
    return np.reshape(emails_flat, (-1, len(mail_format.keys())))

# -------------------
# 3. Notify user of new emails


def get_compiled_regex(dict, key):
    if key in dict:
        return re.compile(dict[key], re.IGNORECASE)
    return re.compile('^$')


def get_notifications(new_emails, mail_format, search_for, inspect_x_last_emails):
    """ Returns a list of notifications to be sent to the user """

    notifications = []
    for s in search_for:
        sender_rgx = get_compiled_regex(s, 'sender')
        subject_rgx = get_compiled_regex(s, 'subject')
        exclude_rgx = get_compiled_regex(s, 'exclude_in_subject')

        # Inspect only the last x new emails (if possible)
        emails_to_inspect = min(inspect_x_last_emails, len(new_emails))

        for i in range(emails_to_inspect):
            curr = new_emails[i]

            sender = re.search(sender_rgx, curr[mail_format['SENDER_EMAIL']])
            subject = re.search(subject_rgx, curr[mail_format['SUBJECT']])
            exclude = re.search(exclude_rgx, curr[mail_format['SUBJECT']])

            # If both sender and subject are specified, then both must match.
            # If only one is specified, then it must match.
            include = False
            if 'sender' in s and 'subject' in s:
                include = sender and subject
            elif 'sender' in s:
                include = sender
            elif 'subject' in s:
                include = subject

            if include and not exclude:
                notifications.append([
                    "Pattern: {}".format(s['name']), 
                    "Sender: {} \n\n{}".format(curr[mail_format['SENDER_EMAIL']], curr[mail_format['SUBJECT']])
                ])

    return notifications


def notify_user(root, notifications):
    """ Prints the notifications to the user """
    for n in notifications:
        subprocess.Popen(['notify-send', n[0], n[1]])
        subprocess.Popen(['paplay', '{}/assets/ring.aif'.format(root)])

if __name__ == "__main__":
    ROOT = "/opt/mail-notifier"

    MAIL_FORMAT = {
        "ACCOUNT_EMAIL": 0,
        "SENDER_EMAIL": 1,
        "SUBJECT": 2
    }

    check_if_valid_installation(ROOT)
    config = read_config(ROOT)

    emails = get_new_emails(MAIL_FORMAT)
    notifications = get_notifications(
        emails,
        MAIL_FORMAT,
        config['search_for'],
        config['inspect_x_last_emails']
    )
    notify_user(ROOT, notifications)
