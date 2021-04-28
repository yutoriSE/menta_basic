import pandas as pd
import eel
import os

CUR_DIR = os.getcwd()


def kimetsu_search(word, csv, dir):

    source = []

    try:

        # csvファイルの読み込み

        df = pd.read_csv(f'{CUR_DIR}/{csv}')
        source = list(df["name"])

        # 検索
        if word in source:
            eel.view_log_js(f'『{word}』はあります')
        else:

            eel.view_log_js(f'『{word}』はありません')
            eel.view_log_js(f'『{word}』追加します')
            source.append(word)

            # CSVの更新
            if not dir:
                df = pd.DataFrame(source, columns=["name"])
                df.to_csv(f'{CUR_DIR}/{csv}', encoding="utf_8-sig")
            else:
                try:
                    df = pd.DataFrame(source, columns=["name"])
                    df.to_csv(f'{dir}/{csv}', encoding="utf_8-sig")
                except:
                    eel.view_log_js(f'{dir}/{csv}に保存できませんでした。パスが誤っています。')

    except OSError:
        eel.view_log_js(f'{CUR_DIR}/{csv}は存在しません')
