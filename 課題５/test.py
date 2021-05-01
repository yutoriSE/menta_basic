import possystem as ps
import pandas as pd

ITEM_MASTER_PATH = 'data.csv'
RECEIPT_DIR = 'receipt'

# マスタ登録
item_list = pd.read_csv(ITEM_MASTER_PATH).values
item_master = []

for il in item_list:
    item_master.append(ps.Item(str(il[0]).zfill(3), il[1], int(il[2])))

# オーダー開始
order = ps.Order(item_master)

order.add_item_order(["001", "12"])

order.view_order_item_info()
