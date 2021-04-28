import time
import datetime
import traceback
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs4
from logging import getLogger, StreamHandler, DEBUG, FileHandler

# Log設定
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
START_DATETIME = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fh = FileHandler('課題２/'+START_DATETIME+'.log', encoding='utf-8')
logger.addHandler(handler)
logger.addHandler(fh)
logger.propagate = False


# クロームドライバーの生成
def set_driver(test_flag):
    option = Options()
    if test_flag:
        option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--incognito')

    return webdriver.Chrome(ChromeDriverManager().install(), options=option)


def main():
    logger.debug('-----------------START-----------------')
    # 検索キーワード
    keyword = input("検索キーワードを入力してください＞")

    driver = set_driver(False)
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

    # データ格納用リスト
    names = []
    places = []
    salarys = []

    # カウンタ
    count = 1

    # 最終ページまで繰り返す
    while True:

        try:
            logger.debug(datetime.datetime.now().strftime(
                '%Y%m%d%H%M%S')+'：'+str(count)+'ページ目のデータ取得')

            # ページソース取得
            html = driver.page_source
            soup = bs4(html, 'lxml')

            # 会社名取得
            names.extend([h3.text for h3 in soup.find_all(
                "h3", class_="cassetteRecruit__name")])

            # テーブル要素の取得
            tables = soup.find_all("table", class_="tableCondition")

            # 勤務地・給与情報抽出
            for table in tables:
                for tr in table.find_all("tr"):
                    if tr.text.split("\n")[1] == "勤務地":
                        places.append(tr.text.split("\n")[2])
                    if tr.text.split("\n")[1] == "給与":
                        salarys.append(tr.text.split("\n")[2])

            # 次へがあれば遷移し、無ければ終了
            if len(driver.find_elements_by_class_name("iconFont--arrowLeft")) > 0:
                driver.find_element_by_class_name(
                    "iconFont--arrowLeft").click()
                count += 1
                time.sleep(3)
            else:
                break

        except:
            logger.debug(datetime.datetime.now().strftime(
                '%Y%m%d%H%M%S')+'：'+traceback.format_exc())

    # データを表に格納
    df = pd.DataFrame(names)
    df[1] = places
    df[2] = salarys
    df.columns = ["会社名", "勤務地", "給与"]

    # csv出力
    df.to_csv("課題２/"+START_DATETIME + "_company_data.csv", index=False)

    logger.debug(str(count)+'ページ：'+str(len(names))+'件のデータを取得しました')
    logger.debug('-----------------END-----------------')


if __name__ == "__main__":
    main()
