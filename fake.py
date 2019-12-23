import json
import requests

url = 'https://api.test.swapix.com/parser/give-ad'
body_register = {'customer_name': "API", 'cost': 223,
                 'name': "Some name", 'description': 'Description',
                 'img_links[]': 'https://img3.goodfon.ru/wallpaper/nbig/f/3e/kaya-scodelario-kaya.jpg',
                 'location_name': 'Gdynia', 'parse_url': 'https://y5426a.ru', 'parser_id': '10', 'category_id': 76}
user_register = requests.post(url, body_register,
                              headers={'Authorization': 'Basic NmZhZjdmYTc3Y2I3NWYwMzRhNGE3NWJjZTgwM2QxMGM='})
print(user_register.json().get("message"))
