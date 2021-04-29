import datetime
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
        self.order_timestamp = ""
        self.order_info = []

    def add_item_order(self, order):
        self.item_order_list.append(order)  # orderは二次元リスト

    # オーダーされた商品の登録有無をチェック（無ければTrueを返す）
    def item_code_check(self, item_code):

        for item in self.item_master:
            if item_code == item.get_item_code():
                return False
        return True

    def order(self):
        self.order_timestamp = datetime.datetime.now()
        while True:
            order_item_code = input("商品コードを入力してください＞")
            if self.item_code_check(order_item_code):
                print(
                    f'【ERROR】商品コード：{order_item_code}は存在しません。正しいコードを入力してください。')
                continue
            order_item_num = input("個数を入力してください＞")
            self.add_item_order([order_item_code, order_item_num])
            if input("お会計の場合は 1 、続ける場合は 2 を入力してください＞") == "1":
                break

    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item[0]))

    # オーダー商品一覧
    def view_order_item_info(self):
        for order in self.item_order_list:
            for item in self.item_master:
                if order[0] == item.get_item_code():
                    info = f'商品名：{item.get_item_name()}  価格：{item.get_price()}円  個数：{order[1]}個  小計：{int(item.get_price())*int(order[1])}円'
                    print(info)
                    self.order_toral_amount += int(item.get_price()
                                                   )*int(order[1])
                    self.order_info.append(info)
        print(f"総額：{self.order_toral_amount}円")

    # 支払い処理
    def calc_payment(self):
        while True:
            self.payment_amount = int(input("お支払い金額を入力してください＞"))
            if self.payment_amount >= self.order_toral_amount:
                print(
                    f'お支払い金額：{self.payment_amount}円  おつり：{self.payment_amount-self.order_toral_amount}円')
                break
            else:
                print("【ERROR】お支払い金額が不足しています。再度ご入力をお願いします。")

    # レシート出力

    def export_receipt(self):
        receipt = open(RECEIPT_DIR+'/'+self.order_timestamp.strftime('%Y%m%d%H%M%S') +
                       '_receipt.txt', 'w', encoding='utf-8')
        receipt_timestamp = self.order_timestamp.strftime('%Y/%m/%d %H:%M:%S')
        receipt.write(f'{receipt_timestamp}\n\n')
        receipt.write('■領収書■\n')
        for info in self.order_info:
            receipt.write(f'{info}\n')
        receipt.write(f'\n総額：{self.order_toral_amount}円\n')
        receipt.write(f'お支払い金額：{self.payment_amount}円\n')
        receipt.write(f'おつり：{self.payment_amount-self.order_toral_amount}円')
        receipt.close()


# メイン処理


def main():
    # マスタ登録
    item_list = pd.read_csv("data.csv").values
    item_master = []

    for il in item_list:
        item_master.append(Item(str(il[0]).zfill(3), il[1], int(il[2])))

    # オーダー登録
    order = Order(item_master)
    order.order()

    # オーダー表示
    # order.view_item_list()

    # オーダー商品情報の表示
    order.view_order_item_info()

    # 支払い処理
    order.calc_payment()

    # レシート出力
    order.export_receipt()


if __name__ == "__main__":
    main()
