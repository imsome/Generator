import config
from DBConnection.Connector import DBConnector
import json


config.db_url = "ip-2441.board"
db_instance = DBConnector()
db_instance.get_filter_groups()


def parse_filter_groups():
    to_parse = db_instance.get_filter_groups()
    root_categories = {}
    categories = []
    for record in to_parse:
        if record[5] is None:
            if record[2] not in root_categories.keys():
                root_categories[record[2]] = []
            root_categories[record[2]].append({record[0]: []})
        else:
            categories.append(record[0])
    return root_categories, categories


def get_filter_group_parents():
    # Возвращает отформатированный словарь имя родителя : айди группы фильтров
    to_parse = db_instance.get_filter_groups()
    group_filter_parent = {}
    for record in to_parse:
        if record[5] is not None:
            if record[5] not in group_filter_parent.keys():
                group_filter_parent[record[5]] = []
            group_filter_parent[record[5]].append({record[0]: []})
    # print(group_filter_parent)
    return group_filter_parent


def get_filter_parents():
    # Возвращает отформатированный словарь имя родителя: айди фильтра-кейса
    to_parse = db_instance.get_filters()
    filter_parent = {}
    for record in to_parse:
        if record[1] is not None:
            if record[1] not in filter_parent.keys():
                filter_parent[record[1]] = []
            filter_parent[record[1]].append({record[0]: []})
    return filter_parent


def get_children_for_filter_group(group_filter_parent):
    filter_parents = get_filter_parents()
    subchildren = subchildren_for_filters()
    for filter_parent in filter_parents:
        for i in range(len(filter_parents[filter_parent])):
            for key in filter_parents[filter_parent][i]:
                filter_parents[filter_parent][i][key] = subchildren.get(key)
    for group_filter in group_filter_parent:
        for children in group_filter_parent[group_filter]:
            for filter_key in children:
                if filter_key not in children.keys():
                    children[filter_key] = "asdasdgsdfg"
                # try:
                # filter_parents[filter_key] = children.get(filter_key)

                children[filter_key] = filter_parents.get(filter_key)

                # i = 0
                # try:
                #     for i in range(len(children[filter_key])):
                #         try:
                #             children[filter_key][i] = subchildren.get(filter_key)
                #         except AttributeError:
                #             children[filter_key][i] = None
                #         i += 1
                # except TypeError:
                #     continue
    return group_filter_parent


def subchildren_for_filters():
    # Собираются подфильтры 2-го уровня, с подгруппами 3-его и подфильтрами подгрупп 3-его
    filter_parents = db_instance.get_filters()
    filters = {}
    for filter in filter_parents:
        if filter[1] not in filters.keys():
            filters[filter[1]] = []
        filters[filter[1]].append(filter[0])
    filter_group_parents = get_filter_group_parents()
    for filter_group_parent in filter_group_parents:
        for filter in range(len(filter_group_parents[filter_group_parent])):
            for filter_id in filter_group_parents[filter_group_parent][filter].keys():
                filter_group_parents[filter_group_parent][filter][filter_id] = filters.get(filter_id)
    return filter_group_parents

    # for filter_group in filter_parents:



def parse_filters():
    root_filters, categories = parse_filter_groups()
    # Получаем каркас для заполнения категорий->фильтров, здесб проставлены категории с фильтрами
    filters_data = db_instance.get_filters()
    filters = {}
    group_filter_parent = get_children_for_filter_group(get_filter_group_parents())
    # Заполняет каркас вариаций фильтров 1-го уровня с детьми-фильтрами 2-го уровня
    for filter in filters_data:
        if filter[1] not in filters.keys():
            filters[filter[1]] = []
        filters[filter[1]].append({filter[0]: group_filter_parent.get(filter[0])})
    # Цикл заполняет вариации фильтров 1-го уровня
    for category in root_filters.keys():
        i = 0
        for root_filter in root_filters[category]:
            for root_filter_key in root_filter.keys():
                root_filter[root_filter_key] = (filters.get(root_filter_key))
            root_filters[category][i] = root_filter
            i += 1
    return root_filters


def dump_json():
    data = parse_filters()
    with open("filters.json", 'w') as json_file:
        json.dump(data, json_file)


# get_filter_parents()
# parse_filters()
# print(subchildren_for_filters())
dump_json()
