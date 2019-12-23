from user_class import User
import config
from config import ReportHandler
from Functions import ruling_functions
from Functions.Admin_panel import AdminController
from DBConnection import Connector
import random


class Generator(object):

    def __init__(self, ads_count=None, users_count=None, watches_count=None, thread_number=None):
        if ads_count is None:
            self.ads_count = config.ads_count
        else:
            self.ads_count = ads_count
        if users_count is None:
            self.users_count = config.users_count
        else:
            self.users_count = users_count
        if watches_count is None:
            self.watches_count = config.watches_count
        else:
            self.watches_count = watches_count
        if thread_number is None:
            self.thread_number = 0
        else:
            self.thread_number = thread_number
        self.ads_to_approve = []

    def generate_ad_example(self):
        ruling_functions.ad_get_new_random_title()
        ruling_functions.ad_get_new_random_description()
        ruling_functions.ad_get_new_random_image()
        ruling_functions.ad_get_new_simple_category()
        ruling_functions.ad_get_new_random_location()
        ruling_functions.ad_get_new_random_cost()
        # ruling_functions.ad_get_new_random_filters()
        if config.dlya_olega:
            config.ad_photos = ["flex.jpg"]

    def generate_ads(self):
        i = 0
        email = config.email
        ReportHandler.parse_log("Generating ads", "Starting generation...")
        while i < self.users_count:
            if self.users_count != 1:
                email_number = 100*int(self.thread_number) + i+1
                email = config.email.format(str(email_number))
            user = User(email, config.password)
            user.register()
            user.authorize()
            i += 1
            curr_ads = 0
            while curr_ads < self.ads_count:
                self.generate_ad_example()
                temp_id = user.create_ad()
                try:
                    if temp_id:
                        config.queue.append(temp_id)
                except TypeError:
                    ReportHandler.add_error("Appending ad id", "Failed")
                finally:
                    curr_ads += 1

    def generate_duplicates(self):
        user = User(config.email, config.password)
        user.register()
        user.authorize()
        user.create_ad()
        user1 = User(config.email.format("1"), config.password)
        user1.register()
        user1.authorize()
        ad_description = "Duplicate description, 1"
        ad_photo = ["r.jpg"]
        ad_category_id = 81
        ad_location_id = 733
        ad_name = "Duplicate_searcher"
        ad_cost = 3500
        user.create_ad(ad_category_id, ad_location_id, config.ad_name, ad_description, config.ad_cost, ad_photo)
        ruling_functions.ad_get_new_hard_category()  # получает новую рандомную категорию с заполненными обязательными фильтрами
        ad_location_id = 734
        ad_photo = ["j.jpg"]
        ad_description = "Duplicate description, 2"
        user1.create_ad(ad_category_id, ad_location_id, config.ad_name, config.ad_description, config.ad_cost, ad_photo)
        user1.create_ad(config.ad_category_id, config.ad_location_id, ad_name, ad_description, config.ad_cost,
                        config.ad_photos)

    def generate_watches(self, ads_min_id, ads_max_id):
        i = 0
        while i < self.users_count:
            i += 1
            user = User(config.email.format(i), config.password)
            user.authorize()
            y = ads_min_id
            while y < self.watches_count + ads_min_id:
                user.watch_ad(random.randint(ads_min_id, ads_max_id))
                y += 1

    def generate_face_ads(self):

        photo = config.face_photos
        user = User(config.email, config.password)
        user.register()
        user.authorize()
        for i in photo:
            photo = user.user_upload_image(i)
            photo = photo["data"]
            photo = photo[0].get("id")
            user.create_ad(ad_photos=photo)

    def generate_statistics_watcher(self, user):

        i = 0
        while i < self.watches_count + 1:
            ad_number = random.randint(1, self.ads_count)
            user.watch_ad(ad_number)
            i += 1

    def generate_statistics(self):
        self.generate_ads()
        ads_getter = Connector.DBConnector()
        ads_getter.approve_adds_with_status_2()
        ads_getter.get_min_and_max_ad_id()
        self.generate_watches(config.min_ad_id, config.max_ad_id)


# TODO def generate_watches(ads_min_id, ads_max_id, user):
    #     user.authorize()
    #     y = ads_min_id
    #     while y < 70 + ads_min_id:
    #         user.watch_ad(random.randint(ads_min_id, ads_max_id))
    #         y += 1
# TODO def increase_watches_counter(watches_count, ad_id):
    #     user = User(config.email, config.password)
    #     user.register()
    #     user.authorize()
    #     i = 0
    #     while i < watches_count:
    #         user.watch_ad(ad_id)
    #         i += 1

    def generate_users(self):
        i = 0
        while i < self.users_count:
            email = config.email.format(i)
            user = User(email, config.password)
            user.register()
            user.authorize()
            i += 1
