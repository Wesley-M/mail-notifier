# Script to install job-notifier

DIR=/opt/job-notifier
if [ -d "$DIR" ]; then
    # Removing the old directory 
    sudo rm -rf /opt/job-notifier
    # Removing the old shortcut
    sudo rm /usr/local/bin/job-notifier
fi

# Create a directory for the script
sudo mkdir /opt/job-notifier

# Copy the script to the directory
sudo cp -r ./ /opt/job-notifier

# Create a shortcut to the script
sudo ln -s /opt/job-notifier/main.py /usr/local/bin/job-notifier
