import config
import json
import random
import os


def get_categories_with_non_required_filters():
    try:
        with open(config.categories_non_required_filters) as file:
            non_required_categories_list = json.load(file)
            return non_required_categories_list
    except FileNotFoundError:
        print("File not found")


def get_categories_with_required_filters():
    try:
        with open(config.categories_required_filters) as file:
            non_required_categories_list = json.load(file)
            return non_required_categories_list
    except FileNotFoundError:
        print("File not found")


def get_only_required_filters_for_category():
    filters = []
    with open(config.categories_with_filters) as file:
        data = json.load(file)
        for category in range(len(data)):
            for key in data[category].keys():
                if str(key) == str(config.ad_category_id):
                    for filter_group in range(len(data[category].get(key))):
                        for filter_group_key in ((data[category].get(key))[filter_group]):
                            current_filter = ((data[category].get(key))[filter_group][filter_group_key])
                            if current_filter.get("required") == "True":
                                filters.append(random.choice(current_filter.get("subfilters")))
    config.ad_filter = filters


def get_filters_for_category(category_id):
    filters = {}
    with open(config.categories_with_filters) as file:
        data = json.load(file)
        for category in range(len(data)):
            for key in data[category].keys():
                if str(key) == str(category_id):
                    for filter_group in range(len(data[category].get(key))):
                        try:
                            for filter_group_key in ((data[category].get(key))[filter_group]):
                                filters[filter_group_key] = []
                                for current_subfilter in ((data[category].get(key))[filter_group][filter_group_key]["subfilters"]):
                                    filters[filter_group_key].append(current_subfilter)
                        except TypeError:
                            continue
    config.ad_filter = filters
    return filters


def ad_get_new_simple_category():
    config.ad_category_id = random.choice(get_categories_with_non_required_filters())


# TODO обработка "тяжелых" категорий, категории с обязательными фильтрами
def ad_get_new_hard_category():
    config.ad_category_id = random.choice(get_categories_with_required_filters())
    get_filters_for_category()


def get_images_repository():
    tree = os.walk(config.images_folder_path)
    paths = []
    for folder in tree:
        if folder[2]:
            for img in folder[2]:
                path = folder[0] + '\\' + img
                paths.append(path)
    config.ad_image_paths = paths
    return paths


def ad_get_new_random_image(images_count=None):
    if not images_count:
        images_count = random.randint(1, 5)
    get_images_repository()
    ad_photos = []
    i = 0
    while i < images_count:
        try:
            config.ad_photos.append(random.choice(config.ad_image_paths))
            ad_photos.append(random.choice(config.ad_image_paths))
            i += 1
        except AttributeError:
            config.ad_photos = [random.choice(config.ad_image_paths)]
            ad_photos = [random.choice(config.ad_image_paths)]
    config.ad_photos = ad_photos
    if config.dlya_olega:
        config.ad_photos = ["flex.jpg"]
        ad_photos = ["flex.jpg"]
    return ad_photos


def ad_get_new_random_title():
    with open(config.titles_path) as json_file:
        data = json.load(json_file)
        random_title = random.choice(data)
        config.ad_name = random_title
        return random_title


def ad_get_new_random_description():
    with open(config.descriptions_path) as json_file:
        data = json.load(json_file)
        random_description = random.choice(data)
        config.ad_description = random_description
        return random_description


def ad_get_new_random_location():
    with open(config.locations_path) as json_file:
        data = json.load(json_file)
        random_location = random.choice(data)
        config.ad_location_id = random_location
        return random_location


def ad_get_new_random_filters(ad_category_id=None):
    if ad_category_id is None:
        ad_category_id = config.ad_category_id
    available_filters = get_filters_for_category(ad_category_id)
    chosen_filters = []
    for filter_id in available_filters.keys():
        chosen_filters.append(random.choice(available_filters.get(filter_id)))
        break


def ad_get_new_random_cost():
    config.ad_cost = random.randint(0, 3000)
    return config.ad_cost


def cut_the_picture(picture):
    print("as")


def rename_pictures():
    path = config.face_photos[0]
    delimeter = path.find('/')
    path = path.split('/')
    last_path = ""
    for i in path:
        if i != path[-1]:
            last_path += i + "/"
    tree = os.walk("Functions/Face_images")
    images_paths = []
    for folder in tree:
        if folder[2]:
            for img in folder[2]:
                path = folder[0] + '\\' + img


ad_get_new_random_filters(111)
