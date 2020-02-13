# -*- coding: utf-8 -*-
from report import Report

#
# HEADERS
#
headers_desk = {'Authorization': 'Basic NmZhZjdmYTc3Y2I3NWYwMzRhNGE3NWJjZTgwM2QxMGM='}
headers_android = {'Authorization': "Basic OTdjNDVhNDI3Mzg5MmFlNTUxNjc2OWFkMzlkMjM4MDI="}
headers_ios = {'Authorization': "Basic NTc4YzY0ZDM3OTA3YWY3YTUwMDczZTgyMjFiYzU4OWI="}
headers_mobile = {'Authorization': "Basic ODliY2U0NmI1Yjc2MmZjMjI2M2FlYTYyNDk1ZWMzNGE="}
headers = {}

#
# MAIN CONFIG
#
url = 'https://{branch}.api.branch.swapix.com/'
admin_url = 'https://{branch}.admin.branch.swapix.com/'
admin_item_url = 'http://{branch}.admin.branch.swapix.com/items/index/edit/{ad_id}'
desktop_url = 'https://{branch}.desktop.branch.swapix.com'
db_url = "{branch}.board"
report_errors_path = 'report_errors.txt'
report_logs_path = 'logs.txt'
email = 'op@op.op'
password = 'opopopop'
is_dump_logs_in_console = True
is_approve = False
is_db_approve = True
threads_count = 5
users_count = 15
watches_count = 3
#
# Paths
#
categories_non_required_filters = "Functions/categories_non_required_filters.json"
categories_required_filters = "Functions/categories_with_required_filters.json"
categories_with_filters = "categories_with_filters.json"
path = "add.json"
ad_filter = "filters.json"
images_folder_path = "Functions/Images"
titles_path = "Functions/titles.json"
descriptions_path = "Functions/descriptions.json"
locations_path = "Functions/locations.json"
face_photos = ["Functions/Face_images/1.jpg", "Functions/Face_images/2.jpg", "Functions/Face_images/3.jpg",
               "Functions/Face_images/4.jpg",
               "Functions/Face_images/5.jpg", "Functions/Face_images/6.jpg", "Functions/Face_images/7.jpg",
               "Functions/Face_images/8.jpg",
               "Functions/Face_images/9.jpg", "Functions/Face_images/10.jpg", "Functions/Face_images/11.jpg",
               "Functions/Face_images/12.jpg"]
face_image = "Functions/Face_images/to_cut.jpg"
#
# Ad variables
#
ad_filters = []
ad_image_paths = []
ads_count = 5
ad_images_count = 1
#
# Ad config
#
ad_category_id = 111
ad_location_id = 350
ad_name = "API_GENERATION_TEST"
ad_description = "PYTHON API TEST UNIQUE"
ad_cost = 200
ad_photos = ["i.jpg"]
#
# AD IDs
#
min_ad_id = 0
max_ad_id = 60
#
# Config vars
#
queue = []  # Очередь для потоков для селениума
ReportHandler = Report(report_errors_path, report_logs_path)
dlya_olega = False
statistic_generation = False
functions = ['cost, location, category, image, description, title']
#
# DB queries
#

