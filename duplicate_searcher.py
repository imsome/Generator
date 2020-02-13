# -*- coding: utf-8 -*-
import argparse
import json

import Threader
from user_class import User
import config
import random
from config import ReportHandler
from Functions import Generator
from Queues import QueueThread
import time
from DBConnection import Connector


def get_attrs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', action='store', dest='email', default='testswapix@gmail.com', help='You can only enter *@*.* email')
    parser.add_argument('--password', action='store', dest='password', default='opopopop')
    parser.add_argument('--url', action='store', dest='url', default="test")
    parser.add_argument('--is_dump_logs_in_console', action='store', dest='is_dump_logs_in_console', default=True)
    parser.add_argument('--users_count', action='store', dest='users_count', default='5')
    parser.add_argument('--is_approve', action='store', dest='is_approve', default=False)
    parser.add_argument('--is_db_approve', action='store', dest='is_db_approve', default=True)
    parser.add_argument('--dlya_olega', action='store', dest='dlya_olega', default=False)
    parser.add_argument('--statistic_generation', action='store', dest='statistic_generation', default=True)
    parser.add_argument('--functions', action='store', dest='functions',
                        default=['cost', 'location', 'category', 'image', 'description', 'title'],
                        help="Attribute helps to create adverts with different settings, "
                             "i.e. you can choose between randomly generated parameters and "
                             "concrete ones. You can change types with .json files in root project folder")
    parser.add_argument('--threads_count', action='store', dest='threads_count', default=5)
    parser.add_argument('--ads_count', action='store', dest='ads_count', default=5)
    parser.add_argument('--watches_count', action='store', dest='watches_count', default=5)
    result = parser.parse_args()
    return result


def set_add_example():
    try:
        with open(config.path, "r") as read_file:
            data = json.load(read_file)
        data = data["data"][0]
        config.ad_category_id = data["category_id"]
        config.ad_location_id = data["location_id"]
        config.ad_name = data["name"]
        config.ad_description = data["description"]
        config.ad_cost = data["cost"]
        config.ad_photos = data["photos"]
        return True

    except FileNotFoundError:
        return False


def create_threads(threads_count, ads_count, users_count, watches_count):
    config.is_approve = False  # сейчас отключено, потому что бессмысленно и беспощадно, все потоки пойдут по одному массиву
    for i in range(threads_count):
        name = "Thread 3%s" % (i + 1)
        my_thread = Threader.Threader(name, i + 1, ads_count, users_count, watches_count)
        my_thread.start()


def url_builder(url):
    if "test" == str(url):
        config.url = 'https://api.test.swapix.com/'
        config.admin_url = 'https://admin.test.swapix.com/'
        config.admin_item_url = 'http://admin.test.swapix.com/items/index/edit/{ad_id}'
    if "pl" in str(url):
        config.url = 'https://api.pl.swapix.com/'
        config.admin_url = 'https://admin.pl.swapix.com/'
        config.admin_item_url = 'http://admin.pl.swapix.com/items/index/edit/{ad_id}'
    if "ng" in str(url):
        config.url = 'https://api.ng.swapix.com/'
        config.admin_url = 'https://admin.ng.swapix.com/'
        config.admin_item_url = 'http://admin.ng.swapix.com/items/index/edit/{ad_id}'
    if "ml" in str(url):
        config.url = 'https://api.ipivi.com/'
        config.admin_url = 'https://admin.ipivi.com/'
        config.admin_item_url = 'http://admin.ipivi.com/items/index/edit/{ad_id}'
    if "ca" in str(url):
        config.url = 'https://api.ca.swapix.com/'
        config.admin_url = 'https://admin.ca.swapix.com/'
        admin_item_url = 'http://admin.ca.swapix.com/items/index/edit/{ad_id}'
    else:
        try:
            int(url)
            config.url = config.url.format(
                branch="ip-" + str(url))
            config.admin_url = config.admin_url.format(
                branch="ip-" + str(url))
            config.admin_item_url = config.admin_item_url.format(branch="ip-" + str(url), ad_id="{ad_id}")
            config.db_url = config.db_url.format(branch="ip-" + str(url))
        except ValueError:
            config.url = config.url.format(
                branch=str(url))
            config.admin_url = config.admin_url.format(
                branch=str(url))
            config.admin_item_url = config.admin_item_url.format(branch=str(url), ad_id="{ad_id}")
            config.db_url = config.db_url.format(branch=str(url))


def queue_start():
    queue = QueueThread.QueueThread()
    queue.start()
    return queue


def queue_end(queue):
    time.sleep(10)
    while not queue.stop_listener():
        time.sleep(3)


def init_app(url):
    clear_previous_logs()
    url_builder(url)
    config.headers = config.headers_mobile
    if config.users_count > 1:
        config.email = config.email[:config.email.find('@')] + "{}" + config.email[config.email.find('@'):]
    ReportHandler.add_log("App initialization", "Trying to configure app")
    if set_add_example():
        ReportHandler.add_log("App initialization", "Configured")
    else:
        ReportHandler.add_log("App initialization",
                              "Failed to load json configs, will work with default settings")
        ReportHandler.add_error("App initialization",
                                "Failed to load json configs, will work with default settings")
    ReportHandler.add_log("Making url", "Configured url with {0}".format(config.url))
    # TODO: обработать вход минимум и максимум айди объяв
    min_ad = 0
    max_ad = 60
    #     пытаемся натроить глобальный реквест объектж


def finish_app():
    ReportHandler.add_log("Finalizing", "Finishing app")
    ReportHandler.print_errors()
    ReportHandler.print_logs()


def clear_previous_logs():
    ReportHandler.print_errors()
    ReportHandler.print_logs()


def main():
    options = get_attrs()
    url = options.url
    config.email = options.email
    config.password = options.password
    config.is_dump_logs_in_console = options.is_dump_logs_in_console
    config.users_count = int(options.users_count)
    config.is_approve = options.is_approve
    config.is_db_approve = options.is_db_approve
    config.dlya_olega = options.dlya_olega
    config.statistic_generation = options.statistic_generation
    config.ads_count = options.ads_count
    config.functions = options.functions
    config.threads_count = options.threads_count
    config.watches_count = options.watches_count
    init_app(url)
    if config.is_approve:  # Флаг аппрува объяв селениумом
        queue = queue_start()
    create_threads(threads_count=config.threads_count, ads_count=config.ads_count, users_count=config.users_count,
                   watches_count=config.watches_count)  # Создание объяв потоками
    if config.is_db_approve:  # Флаг для аппрува объяв с БД
        approve = Connector.DBConnector()
        approve.approve_adds_with_status_2()
    if config.is_approve:  # Мягко выключает очередь для работы с объявами
        queue_end(queue)


if __name__ == '__main__':
    main()
