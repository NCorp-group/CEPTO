#!/usr/bin/env bash

# Set-up python virtual environment
sudo apt update -y && sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    mosquitto \
    mariadb-server

sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service

sudo systemctl enable mariadb.service
sudo systemctl start mariadb.service

# install PIP dependencies
pip install -r requirements.txt