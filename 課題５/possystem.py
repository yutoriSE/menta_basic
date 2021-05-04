import datetime
import os
import eel
import pandas as pd

ITEM_MASTER_PATH = 'data.csv'
RECEIPT_DIR = 'receipt'

# 商品クラス


class Item:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def get_price(self):
        return self.price

    def get_item_code(self):
        return self.item_code

    def get_item_name(self):
        return self.item_name


# オーダークラス


class Order:
    def __init__(self, item_master):
        self.item_order_list = []
        self.item_master = item_master
        self.order_toral_amount = 0
        self.payment_amount = 0
        self.order_timestamp = datetime.datetime.now()
        self.order_info = []
        self.return_amount = -1
        self.history = ""

        # オーダーされた商品の登録有無をチェック（無ければTrueを返す）

    # コードが存在しなければTrueを返す
    def item_code_check(self, item_code):
        for item in self.item_master:
            if item_code == item.get_item_code():
                return False
        return True

    # チェックエラーならTrue
    def add_item_order(self, order):
        if self.item_code_check(order[0]):
            return True
        else:
            self.item_order_list.append(order)  # orderは二次元リスト
            return False

    def view_item_list(self):
        for item in self.item_order_list:
            eel.view_log_js("商品コード:{}".format(item[0]))

    # オーダー商品一覧
    def view_order_item_info(self):

        self.order_toral_amount = 0
        self.order_info = []

        for order in self.item_order_list:
            for item in self.item_master:
                if order[0] == item.get_item_code():
                    info = f'・商品名：{item.get_item_name()}  価格：{item.get_price()}円  個数：{order[1]}個  小計：{int(item.get_price())*int(order[1])}円'
                    eel.view_log_js(info)
                    self.order_toral_amount += int(item.get_price()
                                                   )*int(order[1])
                    self.order_info.append(info)

        eel.view_log_js(f"総額：{self.order_toral_amount}円")

    # 支払い処理

    def calc_payment(self, amount):
        self.payment_amount = int(amount)
        self.return_amount = self.payment_amount-self.order_toral_amount

        if self.payment_amount >= self.order_toral_amount:
            eel.view_log_js(
                f'お支払い金額：{self.payment_amount}円  おつり：{self.payment_amount-self.order_toral_amount}円')
        else:
            eel.view_log_js("【ERROR】お支払い金額が不足しています。再度ご入力をお願いします。")

    # レシート出力

    def export_receipt(self):
        if self.return_amount >= 0:
            path = os.path.join(os.path.dirname(__file__), RECEIPT_DIR,
                                self.order_timestamp.strftime('%Y%m%d%H%M%S')+'_receipt.txt')

            # レシート出力
            receipt = open(path, 'w', encoding='utf-8')
            receipt_timestamp = self.order_timestamp.strftime(
                '%Y/%m/%d %H:%M:%S')
            receipt.write(f'{receipt_timestamp}\n\n')
            receipt.write('■領収書■\n')
            for info in self.order_info:
                receipt.write(f'{info}\n')
            receipt.write(f'\n総額：{self.order_toral_amount}円\n')
            receipt.write(f'お支払い金額：{self.payment_amount}円\n')
            receipt.write(
                f'おつり：{self.payment_amount-self.order_toral_amount}円')
            receipt.close()

            # 販売履歴追加
            self.history = self.order_timestamp.strftime('%Y%m%d%H%M%S')+'   総額：'+str(
                self.order_toral_amount)+'   お支払い金額：'+str(self.payment_amount)+'   おつり：'+str(self.return_amount)
            print(self.history)

    def get_order_toral_amount(self):
        return str(self.order_toral_amount)

    def get_return_amount(self):
        return str(self.return_amount)

    def get_history(self):
        return self.history
