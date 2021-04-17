import threading

from threading import Thread

class DummyHome:
    a = 0

    def __init__(self):
        self.a = 0

    def increment(self):
        self.a = self.a + 1
        print("Inremented a:", self.a)

    def thrd(this):
        for x in range(0,100000):
            this.increment()

home = DummyHome()
home.increment()

thrd = Thread(target = home.thrd)
thrd.start()
thrd.join()
print("Thread is done")
print(home.a)