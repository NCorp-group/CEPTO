# CEPTO

```bash
mosquitto_pub -h 127.0.0.1 -p 1883 -t light_guide/events -m '{"event_type": "notification", "user": {"full_name": "user", "date_of_birth": "1940-01-01"},  "time_of_occurence" : "2021-04-24 23:23:02" }'
```

## Installing Server Database
TODO: kristoffer

## Running the Server
**Pre-requisites:** Linux with apt package manager (shipped with Ubuntu), 
python 3.7 or newer (shipped with Ubuntu), installed and set up MariaDB database
(see "Installing Server Database" above).

Run `web_server\launch.sh`. The script might ask to insert Root password and/or
type `y` or `n` as it installs `python3-pip`, `python3-venv` and Python packages in the background.
All packages are installed on a new separate virtual environment, so they do not
interfere with a pre-existing Python installation.