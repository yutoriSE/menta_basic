import time
import os
import datetime
import traceback
import pandas as pd
import threading
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs4
from logging import getLogger, StreamHandler, DEBUG, FileHandler

# スレッド数
THREAD_NUM = 5

# Log設定
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
START_DATETIME = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fh = FileHandler(os.path.join(os.path.dirname(__file__),
                              'log', START_DATETIME+'.log'), encoding='utf-8')
logger.addHandler(handler)
logger.addHandler(fh)
logger.propagate = False

# 取得データ
data = []

# クロームドライバーの生成


def set_driver(test_flag):
    option = Options()
    if not test_flag:
        option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--incognito')

    return webdriver.Chrome(ChromeDriverManager().install(), options=option)


# ページ内の情報を取得


def scraping_page(url):

    names_page = []
    places_page = []
    salarys_page = []

    driver = set_driver(test_flag=False)
    driver.get(url)

    html = driver.page_source
    soup = bs4(html, 'lxml')

    names_page.extend([h3.text for h3 in soup.find_all(
        "h3", class_="cassetteRecruit__name")])

    # テーブル要素の取得
    tables = soup.find_all("table", class_="tableCondition")

    # 勤務地・給与情報抽出
    for table in tables:
        for tr in table.find_all("tr"):
            if tr.text.split("\n")[1] == "勤務地":
                places_page.append(tr.text.split("\n")[2])
            if tr.text.split("\n")[1] == "給与":
                salarys_page.append(tr.text.split("\n")[2])

    # names.extend(names_page)
    # places.extend(places_page)
    # salarys.extend(salarys_page)

    data.append([names_page, places_page, salarys_page])

    time.sleep(0.5)


# スレッド管理

def control_thread(url):

    # スレッドに空きが出るまで繰り返し
    while True:
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())

        logger.debug(f'実行中のスレッド数：{len(thread_list)}')

        runnable_thread_num = THREAD_NUM - len(thread_list)

        # 空きがあれば実行
        if runnable_thread_num > 0:
            thread = threading.Thread(target=scraping_page, args=(url,))
            thread.start()
            return

        time.sleep(0.5)


def main():
    logger.debug('-----------------START-----------------')
    # 検索キーワード
    keyword = input("検索キーワードを入力してください＞")

    driver = set_driver(test_flag=True)
    driver.get('https://tenshoku.mynavi.jp/')

    time.sleep(3)

    # 閉じるをクリック
    try:
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        logger.debug(datetime.datetime.now().strftime(
            '%Y%m%d%H%M%S')+'：'+traceback.format_exc())

    # フォーム入力し検索
    driver.find_element_by_class_name("topSearch__text").send_keys(keyword)
    driver.find_element_by_xpath(
        "/html/body/div[1]/header/div/div/div[2]/div/form/button").click()

    time.sleep(3)

    # カウンタ
    count = 1

    # 最終ページまで繰り返す
    while True:

        try:
            logger.debug(datetime.datetime.now().strftime(
                '%Y%m%d%H%M%S')+'：'+str(count)+'ページ目のデータ取得')

            # urlをスレッド管理に渡す（スレッド管理側で情報取得）
            control_thread(driver.current_url)

            # 次へがあれば遷移し、無ければ終了
            if len(driver.find_elements_by_class_name("iconFont--arrowLeft")) > 0:
                driver.find_element_by_class_name(
                    "iconFont--arrowLeft").click()
                count += 1
            else:
                break

        except:
            logger.debug(datetime.datetime.now().strftime(
                '%Y%m%d%H%M%S')+'：'+traceback.format_exc())

    # すべてのスレッドの終了を待機
    thread_list = threading.enumerate()
    thread_list.remove(threading.main_thread())

    for thread in thread_list:
        thread.join()

    # データ取り出し
    names = []
    places = []
    salarys = []

    for d in data:
        names.extend(d[0])
        places.extend(d[1])
        salarys.extend(d[2])

    # データを表に格納
    df = pd.DataFrame(names)
    df[1] = places
    df[2] = salarys
    df.columns = ["会社名", "勤務地", "給与"]

    # csv出力
    path = os.path.join(os.path.dirname(__file__),
                        START_DATETIME+"_company_data.csv")
    df.to_csv(path, index=False)

    logger.debug(str(count)+'ページ：'+str(len(names))+'件のデータを取得しました')
    logger.debug('-----------------END-----------------')


if __name__ == "__main__":
    main()
