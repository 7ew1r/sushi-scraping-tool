import requests
from bs4 import BeautifulSoup
import re


class MenuItem:
    def __init__(self, category, name, price,
                 calorie, imageURL):
        self.category = category
        self.name = name
        self.price = price
        self.calorie = calorie
        self.imageURL = imageURL


def menu_to_json(menu_items):
    json_dict = []
    for item in menu_items:
        json_dict.append(convert_to_json(item))
    return json_dict


def convert_to_json(item):
    return {"category": item.category, "name": item.name,
            "price": item.price, "calorie": item.calorie,
            "imageURL": item.imageURL}


def get_category_name(section):
    return section.find('h3', class_='sec-ttl') \
        .find('a', class_='acc-trigger').get_text().replace('\n', '')


def get_menu_items(url):
    html = requests.get(url)
    bs = BeautifulSoup(html.content, "html.parser")

    menu_items = []

    contents = bs.find('div', id='Main').find(
        'div', class_='sec-wrap').find('div', class_='c_l-content')

    # 期間限定/エリア限定, にぎり, 軍艦・巻物, サイドメニュー, ドリンク, デザート
    category_list = ['anchor-sec01', 'anchor-sec03', 'anchor-sec04',
                     'anchor-sec05', 'anchor-sec06', 'anchor-sec07']

    # 期間限定/エリア限定
    for category in category_list:
        section = contents.find('section', id=category)
        category = get_category_name(section)
        item_list = section.find('ul', class_='item-list').find_all('li')

        for item in item_list:
            imageURL = item.find('img')['src']
            title = item.find('span', class_='ttl').get_text()
            price_calorie = item.find('span', class_='price').get_text()
            price = re.search(r'\d+円', price_calorie).group().replace('円', '')
            calorie = re.search(
                r'\d+kcal', price_calorie).group().replace('kcal', '')
            menu_items.append(
                MenuItem(category, title, price, calorie, imageURL))

    return menu_items
