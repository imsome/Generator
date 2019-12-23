import config
import time
from threading import Thread
from Queues.Queuer import Listener


class QueueThread(Thread):
    def __init__(self, name="Queue thread"):
        Thread.__init__(self)
        self.name = name
        self.listener = Listener()

    def run(self):
        self.listener.run()

    def stop_listener(self):
        if self.listener.onWork:
            return False
        self.listener.isListen = False
        return True

