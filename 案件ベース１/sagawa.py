import os
import eel
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4

# 佐川URL
SAGAWA_URL = 'https://k2k.sagawa-exp.co.jp/p/sagawa/web/okurijoinput.jsp'


class Sagawa:

    # クロームドライバーの生成

    def set_driver(self, test_flag):
        option = Options()
        if not test_flag:
            option.add_argument('--headless')
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--ignore-ssl-errors')
        option.add_argument('--incognito')

        return webdriver.Chrome(ChromeDriverManager().install(), options=option)

    def fetch_derivary_status(self, derivery_number, driver: WebDriver):

        # 佐川サイトを開く
        driver.get(SAGAWA_URL)

        # 追跡番号を入力し開始ボタン押下
        driver.find_element_by_id('main:no1').send_keys(derivery_number)
        driver.find_element_by_id('main:toiStart').click()

        # ページが読み込まれるまで待機
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

        # ページソース取得
        html = driver.page_source
        soup = bs4(html, 'lxml')

        table = bs4(
            str(soup.find_all('table', {'class': 'table_basic ttl02'})[0]), 'lxml')

        #table = bs4(soup.find('table', _class='table_basic ttl02'))
        status_text = bs4(str(table.find('td'))).text

        return str(status_text).replace('\t', '').replace('\u3000', '')

    def start_scraping(self, path):

        # カレントフォルダに入力ファイルを置いた場合はファイル名のみで実行可
        if not(":" in path) or ("\\" in path):
            path = os.path.join(os.path.dirname(__file__), path)

        try:
            df = pd.read_excel(path)
        except:
            eel.execute_alert(path+"：ファイルにアクセスできません")
            return

        driver = self.set_driver(False)

        for index, row in df.iterrows():
            # 配達状況の取得
            result = self.fetch_derivary_status(
                row['問い合わせ番号'], driver).split('\n')
            if '' in result:
                result = [r for r in result if r != '']

            # 結果列の更新
            df.iat[index, 2] = result[0]

        df.to_excel(os.path.join(os.path.dirname(__file__),
                                 datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.xlsx'))
        eel.execute_alert("取得完了しました")
