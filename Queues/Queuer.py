import config
import time
from threading import Thread
from Functions.Admin_panel import AdminController


class Listener:

    isListen = True

    def __init__(self, name="Listener"):
        self.name = name
        self.isListen = True
        self.onWork = True
        self.approval = AdminController.AdsApproval()

    def run(self):
        self.approval.start_approve_ads()
        self.on_listen()

    def on_listen(self):
        while self.isListen:
            if len(config.queue) > 0:
                self.onWork = True
                self.approval.approve_ads()
                print(len(config.queue))
            else:
                self.onWork = False
            time.sleep(1)

    def stop_listener(self):
        self.isListen = False
