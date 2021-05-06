import requests
import json
import pandas as pd


def get_api(url):
    result = requests.get(url)
    return result.json()

# json(辞書型)から商品名と価格を抽出する


def extract_item_data(json):

    items = []

    for item in json["Items"]:
        name = item["Item"]["itemName"]
        price = item["Item"]["itemPrice"]
        items.append([name, price])

    return items


def main():
    # キーワード検索結果
    keyword = "鬼滅の刃"
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword={}&applicationId=1070735837086490301".format(
        keyword)
    items = extract_item_data(get_api(url))

    # ランキング検索結果
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1070735837086490301"
    items = extract_item_data(get_api(url))

    # csv出力
    df = pd.DataFrame(items)
    df.columns = ["商品名", "価格"]
    df.to_csv("data.csv", index=False)


def test():
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1070735837086490301"

    assert type(get_api(url)) is dict, f'jsonの取得に失敗しました url:{url}'
    assert len(extract_item_data(get_api(url))
               ) > 0, f'jsonからデータの抽出に失敗しました url:{url}'


main()
