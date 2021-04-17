from threading import Thread

class DummyHome:
    a = 0

    def __init__(self):
        self.a = 0

    def increment(self):
        self.a = self.a + 1

    def thrd(this):
        for x in range(0,30000):
            this.increment()
            print("Incremented a")

home = DummyHome()
home.increment()

thrd = Thread(target = home.thrd)
thrd.start()
while(thrd.is_alive()):
    print(home.a)
thrd.join()
print("Thread is done")