# Set-up python virtual environment
sudo apt update
sudo apt install python3-pip -y
sudo apt install python3-venv -y
python3 -m venv .
source ./bin/activate

# install PIP dependencies
pip install -r requirements.txt

# launch
python3 main.py