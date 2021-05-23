# CEPTO LightGuide


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [CEPTO LightGuide](#cepto-lightguide)
  - [Raspberry PI](#raspberry-pi)
  - [Webserver/Database](#webserverdatabase)
    - [Install dependencies](#install-dependencies)
    - [Setup MariaDB database](#setup-mariadb-database)

<!-- /code_chunk_output -->


## Raspberry PI

## Webserver/Database

### Setup MariaDB database

 ```sh
    
 ```
### Install dependencies

**TODO** 

Source the `web_server/launch.sh` with root permissions. If the script is not executable, then first change its file permissions with the following commands:
```sh
    chmod u+x web_server/launch.sh
```

The script can then the executed with the following command:
```sh
    sudo ./web_server/launch.sh
```





```bash
mosquitto_pub -h 127.0.0.1 -p 1883 -t light_guide/events -m '{"event_type": "notification", "user": {"full_name": "user", "date_of_birth": "1940-01-01"},  "time_of_occurence" : "2021-04-24 23:23:02" }'
```