import kura


def test_convert_to_json():
    item = kura.MenuItem('カテゴリー', '名前', 100, 'エリア',
                         100, '可', 'http://example.com')
    expect = {"category": 'カテゴリー', "name": '名前',
              "price": 100,  "area": 'エリア', "calorie": 100, "canTakeOut": '可',
              "imageURL": item.imageURL}

    assert kura.convert_to_json(item) == expect
