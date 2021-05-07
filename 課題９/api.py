from os import name
import time
import datetime
import traceback
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twitter import Twitter, OAuth

# Twitter
ACCESS_TOKEN = "1390651064546840576-VIWa79IFmYzNdzxbHfUDZCkYEbJLj8"
ACCESS_TOKEN_SECRET = "fAyZzkyMImXXRzK4NgC48XpzESaBe3VzN7nwegD57DqGW"
API_KEY = "2YRsJT547MU3p5RVPGqQoTv2B"
API_SECRET = "jIRfSAwl0N5mLY0YKHTWgEhv7JoOQgvjL58igQyvrzjrObyauE"


def set_driver(test_flag):
    option = Options()
    if not test_flag:
        option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--incognito')

    return webdriver.Chrome(ChromeDriverManager().install(), options=option)


# カート追加ボタンが存在すればTrueを返す


def exists_stock(url):
    driver = set_driver(test_flag=True)
    driver.get(url)
    # ページが読み込まれるまで待機
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

    try:
        element = driver.find_element_by_id('addToCart_feature_div')
        name = driver.find_element_by_id('productTitle').text
    except:
        driver.close()
        print(traceback.format_exc())
        return [False, ""]

    driver.close()
    return [True, name]


def main():

    tweet_flag = True

    while True:

        # 在庫確認
        result = exists_stock('https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-SHARP-SJ-AF50G-R-%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC-%E3%82%B0%E3%83%A9%E3%83%87%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%AC%E3%83%83%E3%83%89/dp/B07Z7M52LG?ref_=fspcr_pl_dp_2_2272928051&th=1')

        # 在庫があればツイートする
        if result[0] and tweet_flag:
            t = Twitter(auth=OAuth(
                ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET))

            t.statuses.update(status=result[1][:50]+'...の在庫はありました')

            tweet_flag = False

            print("ツイートしました。")

        elif not result[0]:
            # 在庫が無くなったらツイートを許可する
            tweet_flag = True
            print('在庫はありません')

        time.sleep(5)


if __name__ == "__main__":
    main()
