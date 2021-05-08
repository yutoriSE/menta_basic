import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4

#佐川URL
SAGAWA_URL = 'https://k2k.sagawa-exp.co.jp/p/sagawa/web/okurijoinput.jsp'

# クロームドライバーの生成
def set_driver(test_flag):
    option = Options()
    if test_flag:
        option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--incognito')

    return webdriver.Chrome(ChromeDriverManager().install(), options=option)


def fetch_derivary_status(derivery_number, driver:WebDriver):

    #追跡番号を入力し開始ボタン押下
    driver.find_element_by_id('main:no1').send_keys(derivery_number)
    driver.find_element_by_id('main:toiStart').click()

    # ページが読み込まれるまで待機
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

    # ページソース取得
    html = driver.page_source
    soup = bs4(html, 'lxml')

    table = bs4(str(soup.find_all('table', {'class': 'table_basic ttl02'})[0]), 'lxml')

    #table = bs4(soup.find('table', _class='table_basic ttl02'))
    status_text = bs4(table.find('td')).text

    return str(status_text).replace('\n', '')

def main():
    path = os.path.join(os.path.dirname(__file__), '佐川フォーマット.xlsx')
    df = pd.read_excel(path)

    driver = set_driver(False)
    driver.get(SAGAWA_URL)
    
    for index, row in df.iterrows():
        #配達状況の取得
        result = fetch_derivary_status(row['問い合わせ番号'] , driver)
        #結果列の更新
        df.at[index, '問い合わせ番号'] = result

    
    df.to_excel(os.path.join(os.path.dirname(__file__), '佐川フォーマット_更新.xlsx'))


main()

