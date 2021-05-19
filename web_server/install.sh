# Set-up python virtual environment
sudo apt update
sudo apt install python3-pip -y
sudo apt install python3-venv -y
python3 -m venv .
source ./bin/activate

# install PIP dependencies
pip install -r requirements.txt

# install and set-up MariaDB
sudo apt install mariadb-server

# TODO: finish setting up mariadb user and source database