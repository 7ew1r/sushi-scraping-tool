import json
import kura
import sushiro
import click


def output_json(file_path, menu_json):
    with open(file_path, "w") as json_file:
        json.dump(menu_json, json_file)


@click.command(help='sushi-scraping-tool')
@click.option('-s', '--source', 'src',
              type=click.Choice(['kura', 'sushiro'], case_sensitive=False),
              help='kura: くら寿司, sushiri: スシロー', required=True)
def main(src):
    menu_items = []
    menu_json = ""
    file_path = ""

    if(src == "kura"):
        url = "https://www.kurasushi.co.jp/menu/?area=area0"
        menu_items = kura.get_menu_items(url)
        menu_json = kura.menu_to_json(menu_items)
        file_path = './kura.json'
    elif (src == "sushiro"):
        url = "https://www.akindo-sushiro.co.jp/menu/"
        menu_items = sushiro.get_menu_items(url)
        menu_json = sushiro.menu_to_json(menu_items)
        file_path = './sushiro.json'

    output_json(file_path, menu_json)


if __name__ == '__main__':
    main()
