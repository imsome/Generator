# -*- coding: utf-8 -*-
import config
from config import ReportHandler
from Functions import ruling_functions as Rule
import json
import requests
import api_requests
import random
import datetime


class User(object):

    __variable = "asd"

    def __init__(self, mail=None, password=None, delimeter=None, name="opop"):
        if delimeter is not None:
            self.mail = mail[:mail.find('@')] + "+" + str(delimeter) + mail[mail.find('@'):]
        else:
            self.mail = mail
        self.name = name
        self.password = password
        self.token = None
        self.jwt_token = None

    def register(self):
        ReportHandler.add_log("Registration", "Registering with user {0}".format(self.mail))
        url = config.url + api_requests.register
        body_register = {'name': self.name + datetime.datetime.now().strftime("%H:%M:%S.%f"), 'email': self.mail,
                         'password': self.password}
        user_register = requests.post(url, body_register, headers=config.headers_desk)
        return self.token_builder(user_register.json(), "Registration")

    def authorize(self):

        ReportHandler.add_log("Authorization", "Authorizing with user {0}".format(self.mail))
        url = config.url + api_requests.authorize
        body_login = {'email': self.mail, 'password': self.password}
        user_login = requests.post(url, body_login, headers=config.headers_desk)
        data = user_login.json()
        return self.token_builder(data, "Authorization")

    def update_name(self, new_name):
        ReportHandler.add_log("Updating", "Updating user name with {0}".format(self.mail))
        url = config.url + api_requests.update_user
        body_update = {'token': self.token, 'name': new_name}
        update_name = requests.post(url, body_update, headers=config.headers)
        ReportHandler.report_it("Updating name", update_name.json())

    def set_language(self, new_language):
        ReportHandler.add_log("Setting new language", "Setting new language for user {0}".format(self.mail))
        url = config.url + api_requests.set_new_language
        body_update = {'token': self.token, 'language': new_language}
        update_language = requests.put(url, body_update)
        ReportHandler.report_it("Updating language", update_language.json())

    # def update_phone(self):
    #     print("TODO_IT")

    def token_builder(self, data=None, function=None):
        ReportHandler.response_token(function, data)
        if data.get('data'):
            try:
                self.token = data['token']
            except KeyError:
                data = data.get('data')
                data = data[0]
                self.token = data.get('token')
        else:
            return False

    def watch_ad(self, ad_id):
        # trying_to_watch_ad
        ReportHandler.add_log("Watching add", "Trying to watch ad with id {0}".format(ad_id))
        url = config.url + api_requests.watch_ad
        param = {'token': self.token}
        view_ad = requests.get(url + str(ad_id), headers=config.headers, params=param)
        ReportHandler.report_it("Watching add", view_ad.json())

    def watch_random_ad(self):
        ad_id = random.randint(config.min_ad_id, config.max_ad_id)
        ReportHandler.add_log("Watching random add", "Trying to watch random add with id {0}".format(ad_id))
        url = config.url + api_requests.watch_ad
        param = {'token': self.token}
        view_ad = requests.get(url + str(ad_id), headers=config.headers_desk, params=param)
        ReportHandler.report_it("Watching random add", view_ad.json())

    def user_upload_image(self, path=None):
        ReportHandler.add_log("Upload image", "Trying to upload random image")
        url = config.url + api_requests.upload_image
        if path is None:
            photo_path = Rule.ad_get_new_random_image()[0]
        else:
            photo_path = path
        body_upload = {'token': self.token}
        upload_image = requests.post(url, body_upload, headers=config.headers_desk,
                                     files={'image': open(photo_path, 'rb')})
        data = upload_image.json()
        img_id = data.get('data')
        ReportHandler.report_it("Upload image", data)
        return upload_image.json()

    def create_ad_old(self, ad_category_id=None, ad_location_id=None, ad_name=None, ad_description=None, ad_cost=None,
                      ad_photos=None):
        if ad_category_id is None:
            ad_category_id = config.ad_category_id
        if ad_location_id is None:
            ad_location_id = config.ad_location_id
        if ad_name is None:
            ad_name = config.ad_name
        if ad_description is None:
            ad_description = config.ad_description
        if ad_cost is None:
            ad_cost = config.ad_cost
        if ad_photos is None:
            ad_photos = config.ad_photos
        ReportHandler.add_log("Creating add", "Trying to create add with your settings")
        url = config.url + api_requests.create_ad
        body_add = {'category_id': ad_category_id, 'location_id': ad_location_id, 'name': ad_name,
                    'description': ad_description,
                    'cost': ad_cost, 'token': self.token}
        creating_add = requests.post(url, body_add, headers=config.headers_desk,
                                     files={'photos[]': open(ad_photos[0], 'rb')})
        ReportHandler.report_it("Creating add", creating_add.json())

    def create_ad(self, ad_category_id=None, ad_location_id=None, ad_name=None, ad_description=None, ad_cost=None,
                  ad_photos=None, ad_filters=None):
        if ad_category_id is None:
            ad_category_id = config.ad_category_id
        if ad_location_id is None:
            ad_location_id = config.ad_location_id
        if ad_name is None:
            ad_name = config.ad_name
        if ad_description is None:
            ad_description = config.ad_description
        if ad_cost is None:
            ad_cost = config.ad_cost
        if ad_filters is None:
            ad_filters = config.ad_filters
        if type(ad_photos) == int:
            ad_photos = ad_photos
        elif ad_photos is None:
            ad_photos = self.parse_photo()
        ReportHandler.add_log("Creating add", "Trying to create add with your settings")
        url = config.url + api_requests.advert_create
        body_add = {"category_id": ad_category_id, "location_id": ad_location_id, "name": ad_name,
                    "description": ad_description, "ad_filters[]": ad_filters, "cost": ad_cost, "token": self.token, "image_ids[]": ad_photos}
        creating_add = requests.post(url, body_add, headers=config.headers_desk)
        ReportHandler.report_it("Creating add", creating_add.json())
        try:
            return creating_add.json().get("data")[0].get("id")
        except IndexError:
            return False

    def parse_photo(self):
        images = []
        for i in range(len(config.ad_photos)):
            image = self.user_upload_image()
            # TODO запилить разделение на дубль/не дубль в массивах (ибо половина объяв тупа падает)
            if image.get('success'):
                curr_image = image.get('data')[0]
                images.append(curr_image.get('id'))
        return images

