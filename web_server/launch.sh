#!/usr/bin/env bash

# Set-up python virtual environment
sudo apt update -y && sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    mosquitto \
    mariadb-server
# sudo apt install python3-pip -y
# sudo apt install python3-venv -y

sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service

sudo systemctl enable mariadb.service
sudo systemctl start mariadb.service

echo -e "TYPE:\n\tGRANT ALL ON *.* TO 'testuser'@'localhost' IDENTIFIED BY 'test' WITH GRANT OPTION;"

sudo mariadb

if [ ! -f ./bin/activate ]; then 
    /usr/bin/python3 -m venv .
fi

source ./bin/activate

# install PIP dependencies
pip install -r requirements.txt

# launch
# python3 main.py