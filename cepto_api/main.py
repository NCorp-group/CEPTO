import subprocess as sp
import time

if __name__ == "__main__":
    p2 = sp.Popen(['python', 'front_api.py'])

    time.sleep(10)