import subprocess as sp
import time

if __name__ == "__main__":
    p2 = sp.Popen(['python', 'back_api.py'])
    p1 = sp.Popen(['python', 'front_api.py'])

    time.sleep(5)
    print("Server launch complete")