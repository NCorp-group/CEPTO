#!/usr/bin/env bash

set -e

# download mariaDB, mosquitto-broker, zigbee2mqtt, npm, nodejs
# setup mariaDB testuser

# check if services are running!

update_and_install_build_requirement_packages() {
    sudo apt update
    sudo apt install -ygit make g++ gcc
}

install_and_setup_mosquitto_broker() {
    sudo apt install -y mosquitto
    sudo systemctl enable mosquitto.service
    sudo systemctl start mosquitto.service
}

install_nodejs() {
    sudo curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    sudo apt install -y nodejs
}

install_and_setup_zigbee2mqtt() {
    if [ -d /opt/zigbee2mqtt ] && [ systemctl status zigbee2mqtt 2&>1 /dev/null ]; then
        return
    fi
    
    # copy service file
    if [ ! -f setup/zigbee2mqtt.service ]; then 
        cp setup/zigbee2mqtt.service /etc/systemd/system/zigbee2mqtt.service
    fi
    
    sudo git clone https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
    sudo chown -R ${USER}:${USER} /opt/zigbee2mqtt
    cd /opt/zigbee2mqtt
    npm ci --production

    # setup systemd service
    sudo systemctl enable zigbee2mqtt.service
    sudo systemctl start zigbee2mqtt
}

install_and_setup_mariaDB() {
    local DB_USER="testuser"
    local DB_PASSWD="test"
    local CREATE_USER_QUERY="CREATE USER '${DB_USER}'@localhost IDENTIFIED BY '${DB_PASSWD}';"

    sudo apt install -y mariadb-server
    if [ ! -f setup/create_tables.sql ]; then return -1; fi
    sudo systemctl enable mariadb.service
    sudo systemctl start mariadb.service
    mysql -u "root" -p "root" -e "source setup/create_tables.sql"
}

update_and_install_build_requirement_packages
install_nodejs
install_and_setup_mosquitto_broker
install_and_setup_mariaDB
install_and_setup_zigbee2mqtt

echo -e "setup complete!\n"
echo -e ""
