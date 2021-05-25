import subprocess as sp
import time

if __name__ == "__main__":
    p2 = sp.Popen(['python3', 'back_api.py'])
    p1 = sp.Popen(['python3', 'front_api.py'])

    time.sleep(5)
    print("Server launch complete")
