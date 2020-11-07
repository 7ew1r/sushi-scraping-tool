import requests
from bs4 import BeautifulSoup


class MenuItem:
    def __init__(self, category, name, price, area,
                 calorie, canTakeOut, imageURL):
        self.category = category
        self.name = name
        self.price = price
        self.area = area
        self.calorie = calorie
        self.canTakeOut = canTakeOut
        self.imageURL = imageURL


def menu_to_json(menu_items):
    json_dict = []
    for item in menu_items:
        json_dict.append(convert_to_json(item))
    return json_dict


def convert_to_json(item):
    return {"category": item.category, "name": item.name,
            "price": item.price, "area": item.area,
            "calorie": item.calorie, "canTakeOut": item.canTakeOut,
            "imageURL": item.imageURL}


def get_menu_items(url):
    html = requests.get(url)
    bs = BeautifulSoup(html.content, "html.parser")

    menu_items = []

    menu_sections = bs.find_all('section', class_='menu-section')
    for section in menu_sections:
        category = section.find('h3', class_='menu-section-heading').get_text()
        menu_items_tag = section.select('.menu-item')

        for item in menu_items_tag:
            name = item.find('h4', class_='menu-name').get_text()

            url_prifix = "https://www.kurasushi.co.jp"
            imageURL = url_prifix + item.find('img')['src']

            li_tags = item.find_all('li')
            price = li_tags[0].find_all('p')[0].get_text()[:-5]
            calorie = li_tags[0].find_all('p')[1].get_text()[:-4]

            # 提供エリアが書かれていないメニューがある
            if '【提供エリア】' in li_tags[1].find('p').get_text():
                area = li_tags[1].find_all('p')[-1].get_text()
            elif '【お持ち帰り】' in li_tags[1].find('p').get_text():
                area = '情報なし'
                canTakeOut = li_tags[1].find_all('p')[-1].get_text()

            if len(li_tags) >= 3:
                if '【お持ち帰り】' in li_tags[2].find('p').get_text():
                    canTakeOut = li_tags[2].find_all('p')[-1].get_text()

            menu_items.append(MenuItem(category, name,  price,
                                       area, calorie, canTakeOut, imageURL))

    return menu_items
