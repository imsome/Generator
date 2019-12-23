from threading import Thread
import config
from DBConnection import Connector
import time

from Functions import Generator


class Threader(Thread):

    def __init__(self, name, thread_number, ads_count=10, users_count=10, watches_count=60):
        Thread.__init__(self)
        self.name = name
        self.thread_number = thread_number
        self.ads_count = ads_count
        self.users_count = users_count
        self.watches_count = watches_count

    def run(self):
        generator = Generator.Generator(ads_count=self.ads_count, users_count=self.users_count,
                                        watches_count=self.watches_count, thread_number=self.thread_number)
        if config.statistic_generation:
            generator.generate_statistics()
        else:
            generator.generate_ads()
            if config.is_db_approve:
                approve = Connector.DBConnector()
                approve.approve_adds_with_status_2()
