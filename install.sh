# Script to install job-notifier

DIR=/opt/mail-notifier
if [ -d "$DIR" ]; then
    # Removing the old directory 
    sudo rm -rf /opt/mail-notifier
    # Removing the old shortcut
    sudo rm /usr/local/bin/mail-notifier
fi

# Create a directory for the script
sudo mkdir /opt/mail-notifier

# Copy the script to the directory
sudo cp -r ./ /opt/mail-notifier

# Create a shortcut to the script
sudo ln -s /opt/mail-notifier/main.py /usr/local/bin/mail-notifier
