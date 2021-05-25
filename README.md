# CEPTO LightGuide


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [CEPTO LightGuide](#cepto-lightguide)
  - [Cloning the repository](#cloning-the-repository)
  - [Raspberry PI](#raspberry-pi)
    - [Install NodeJS](#install-nodejs)
    - [Zigbee2mqtt](#zigbee2mqtt)
    - [Mosquitto-broker](#mosquitto-broker)
  - [# Install paho-mqtt](#-install-paho-mqtt)
    - [Running the program](#running-the-program)
  - [Webserver/Database](#webserverdatabase)
    - [Install dependencies](#install-dependencies)
    - [Setup MariaDB database](#setup-mariadb-database)
    - [Running the web server](#running-the-web-server)

<!-- /code_chunk_output -->
## Cloning the repository
Open your preferred termminal

Navigate to the directory where you want to clone the CEPTO Light Guide repository, and execute the following:

```shell=sh
git clone https://github.com/NCorp-group/CEPTO.git
```

## Raspberry PI

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

## # Install paho-mqtt
```shell=sh
pip3 install paho-mqtt
```
### Running the program
Head to `CEPTO/light_guide/production/` in the cloned repository.
```shell=sh
python LightGuideHome.py <web_server_ip>
```

## Webserver/Database

### Install dependencies

**TODO** 

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
CREATE USER 'testuser'@localhost IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON *.* TO 'testuser'@localhost IDENTIFIED BY 'test';
```

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


