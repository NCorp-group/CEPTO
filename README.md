# CEPTO LightGuide


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [CEPTO LightGuide](#cepto-lightguide)
  - [Cloning the repository](#cloning-the-repository)
  - [Requirements](#requirements)
    - [Hardware](#hardware)
    - [Software](#software)
  - [Raspberry PI](#raspberry-pi)
    - [Install NodeJS](#install-nodejs)
    - [Zigbee2mqtt](#zigbee2mqtt)
    - [Mosquitto-broker](#mosquitto-broker)
  - [Install paho-mqtt](#-install-paho-mqtt)
    - [Running the program](#running-the-program)
  - [Webserver/Database](#webserverdatabase)
    - [Install dependencies](#install-dependencies)
    - [Setup MariaDB database](#setup-mariadb-database)
    - [Running the web server](#running-the-web-server)

<!-- /code_chunk_output -->
## Cloning the repository
Open your preferred terminal

Navigate to the directory where you want to clone the CEPTO Light Guide repository, and execute the following:

```shell=sh
git clone https://github.com/NCorp-group/CEPTO.git
```

## Requirements
To setup the entire project you will need the following list of hardware- and software components.

### Hardware

| Component | Quantity | Tested with |
|-----------|----------|-------------|
| Raspberry Pi 4B | 1 Raspberry Pi | 1 Raspberry Pi 4B 4GB RAM |
| [Supported zigbee adapter](https://www.zigbee2mqtt.io/getting_started/what_do_i_need.html#supported-zigbee-adapter) | 1 adapter | 1 [Texas Instruments CC2531](https://www.zigbee2mqtt.io/information/supported_adapters.html) | 
| [Xiaomi RTCGQ11LM (PIR sensors)](https://www.zigbee2mqtt.io/devices/RTCGQ11LM.html) | At least 3 sensors | 5 sensors |
| [Gledopto GL-MC-001P (Light strips)](https://www.zigbee2mqtt.io/devices/GL-MC-001P.html) | At least 3 light strips | 5 light strips |

### Software
|Component | Tested with |
|----------|-------------|
| [Ubuntu Server](https://ubuntu.com/download/server) | Version 20.04 LTS |
| [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit) | 2021-03-04 release |
| [MariaDB relational database](https://mariadb.org/) | Version 10.5.9 | 
| [zigbee2mqtt](https://github.com/koenkk/zigbee2mqtt) | Version 1.18.3 |


## Raspberry PI

### Pair devices

Please follow the documentation for pairing the light strips and PIR sensors:

**Light strip:** https://www.zigbee2mqtt.io/devices/GL-MC-001P.html

**PIR sensor:** https://www.zigbee2mqtt.io/devices/RTCGQ11LM.html

A configuration example for the zigbee2mqtt devices can be found at ``CEPTO/light_guide/setup/configuration.yaml``, this has been used during development and tested.

### Install NodeJS
```
sudo curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install -y nodejs
```

### Zigbee2mqtt
Navigate to the root directory of the CEPTO repository.


```shell=sh
# copy service file
sudo cp light_guide/setup/zigbee2mqtt.service /etc/systemd/system/

sudo git clone https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt

sudo chown -R ${USER}:${USER} /opt/zigbee2mqtt

cd /opt/zigbee2mqtt

npm ci --production


# setup systemd service
sudo systemctl enable zigbee2mqtt.service

sudo systemctl start zigbee2mqtt
```

### Mosquitto-broker

```shell=sh    
sudo apt install -y mosquitto
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service
```

### Install paho-mqtt
```shell=sh
pip3 install paho-mqtt
```
### Running the program
Make sure to have set the correct friendly names in the configuration file at ``CEPTO/light_guide/production/config.json``, the default should match ``CEPTO/light_guide/setup/configuration.yaml``.

Head to the root of the cloned `CEPTO` repository.
```shell=sh
python3 light_guide/production/LightGuideHome.py <web_server_ip>
```

## Webserver/Database

### Install dependencies

Source the `web_server/launch.sh` with root permissions. If the script is not executable, then first change its file permissions with the following commands:
```sh
chmod u+x web_server/install.sh
```

The script can then the executed with the following command:
```sh
sudo ./web_server/install.sh
```

### Setup MariaDB database

Start a MariaDB session:

 ```sh
sudo mariadb
 ```
First create the database user, and assign appropriate permissions:

```sql
CREATE USER 'lg_user'@localhost IDENTIFIED BY 'lg_password';
GRANT ALL PRIVILEGES ON *.* TO 'lg_user'@localhost IDENTIFIED BY 'lg_password';
```
Logout of the mariadb root shell (either type `exit` or type `ctrl+D`), and login to the newly created user account:

 ```sh
mysql -u lg_user -p
 ```
 
 You will be prompted to type the password. Type `lg_password`.

Then setup and create the database schema:
```sql
SOURCE <path_to>/CEPTO/web_server/database/create_tables.sql;
```

Where `path_to` is the absolute path to the directory where you cloned the repository e.g. `/home/user/`. To get the absolute path to your current position use the command `pwd`.

### Running the web server

To start the web server run:
```shell=sh
python3 web_server/main.py
```

The web server should now be running and listening for requests on port `5000`. To test that a client can connect to the server you can run the command:

```shell=sh
curl http://localhost:5000/echo/hello
```

If you get no error and `hello` is returned the server is working correctly!


