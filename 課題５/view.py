import eel
import os
import desktop
import possystem as ps
import pandas as pd

ITEM_MASTER_PATH = 'data.csv'
RECEIPT_DIR = 'receipt'

app_name = 'html'
end_point = "index.html"
size = (1200, 800)

# マスタ登録
item_list = pd.read_csv(ITEM_MASTER_PATH).values
item_master = []

for il in item_list:
    item_master.append(ps.Item(str(il[0]).zfill(3), il[1], int(il[2])))

# オーダー開始
order = ps.Order(item_master)

# オーダー追加
@ eel.expose
def add_order(item_code, item_num):
    order.add_item_order([item_code, item_num])

# オーダー情報表示
@ eel.expose
def view_order_item_info():
    order.view_order_item_info()

# 支払い処理
@ eel.expose
def calc_payment(amount):
    order.calc_payment(amount)

# レシート出力
@ eel.expose
def export_receipt():
    order.export_receipt()

# 総額を返す
@ eel.expose
def get_total_amount():
    return order.get_order_toral_amount()

# おつりを返す
@ eel.expose
def get_return_amount():
    return order.get_return_amount()


desktop.start(app_name, end_point, size)
