# Mail Notifier

**Mail Notifier** is a simple tool that notifies you when there is new mail in your inbox. 
The thing is, it is smart enough to understand **what** to notify you. It looks at patterns 
in a config file and follows them when trying to notify.

This script relies on (mailnag)[https://github.com/pulb/mailnag] to work (In fact, it is just a
user script that mailnag will run when there is new mail). So, you need to install mailnag first. It also
makes use of (_notify-send_)[https://wiki.archlinux.org/index.php/Desktop_notifications] from libnotify 
to send desktop notifications and the (_pacat_)[https://man.archlinux.org/man/pacat.1] tool from PulseAudio.

## Installation & Instructions

1. First install mailnag, more info on [the mailnag repository](https://github.com/pulb/mailnag/);

2. Make sure you have the following packages installed: `libnotify`, `pulseaudio`, `python3`;

```bash
user@pc ~> pulseaudio --version
pulseaudio x.x.x
user@pc ~> notify-send --version
notify-send x.x.x
user@pc ~> python3 --version
Python 3.x.x
```

3. To "install" the script, just clone this repository and run the `install.sh` script. Make
sure all scritps are executable beforehand.

```bash
user@pc ~/mail-notifier> chmod +x main.py install.sh
```

4. In mailnag, add your preffered account and in the plugin tab only enable **User Script**. You
will need to add the path to the script. It should be: "/usr/local/bin/mail-notifier".

5. The script will look for a config file in /opt/mail-notifier/config.json. So you can 
just copy the following example config file to that location and edit it to your liking.

```js
{
    "search_for": [
        {
            "name": "Pattern name",
            "sender": ".*example.*",
            "subject": ".*example.*",
            "exclude_in_subject": ".*undesirable.*",
        }
    ],
    "inspect_x_last_emails": 10
}
```