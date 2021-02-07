import csv
import datetime
import eel
import os


fieldnames = ['CODE', 'NAME', 'PRICE', 'QUANTITY', 'TOTAL']


def main():
    eel.init("web")
    eel.start("index.html")


@eel.expose
def display_inventory():

    existing_products_list = []
    existing_products_list.append(fieldnames)

    with open('product_master.csv', 'r') as rewrite_csv:
        existing_products = csv.DictReader(rewrite_csv)
        for existing_product in existing_products:
            existing_product_list = []
            existing_product_list.append(existing_product['CODE'])
            existing_product_list.append(existing_product['NAME'])
            existing_product_list.append(existing_product['PRICE'])
            existing_product_list.append(existing_product['QUANTITY'])
            existing_product_list.append(existing_product['TOTAL'])
            existing_products_list.append(existing_product_list)

    return existing_products_list

@eel.expose
def register_inventory(product_code, product_name, product_price, product_quantity, product_total):

    with open('product_master.csv', 'a') as add_to_csv:
        writer = csv.DictWriter(add_to_csv, fieldnames=fieldnames)
        writer.writerow({
            'CODE': product_code,
            'NAME': product_name,
            'PRICE': product_price,
            'QUANTITY': product_quantity,
            'TOTAL': product_total,
        })

    return '登録できました！\n更新された在庫情報を確認したい場合は、一番上の「現在の在庫を確認する」をクリックしてね！'

@eel.expose
def update_inventory(list_of_purchased_items):

    with open('product_master.csv', 'r', encoding='UTF-8') as rf:
        reader = csv.reader(rf)
        # ヘッダー行を飛ばす
        next(reader)

        with open("product_master.csv", 'w', encoding='UTF-8') as wf:
            writer = csv.writer(wf)
            writer.writerow(['CODE', 'NAME', 'PRICE', 'QUANTITY', 'TOTAL'])
            # 購入された分だけ在庫数を減らす
            for index, line in enumerate(reader):
                if line[0] == list_of_purchased_items[index][0]:
                    line[3] = int(line[3]) - int(list_of_purchased_items[index][3])
                    line[4] = int(line[2]) * int(line[3])
                    writer.writerow([line[0], line[1], line[2], line[3], line[4]])
                else:
                    pass

@eel.expose
def output_receipt(payment_amount, sum_total_output, change, list_of_purchased_items):
    now = datetime.datetime.now()
    output_receipt_time = now.strftime('%Y_%m%d_%H%M')
    time_for_receipt = now.strftime('%Y年%m月%d日 %H時%M分')
    sum_total_output = "{:,}".format(sum_total_output)
    payment_amount = "{:,}".format(payment_amount)
    change = "{:,}".format(change)
    purchased_items_info = ''
    for index, list_of_purchased_item in enumerate(list_of_purchased_items):
        purchased_item_info = ''
        purchased_item_info = f'{list_of_purchased_item[1]}\n@¥{list_of_purchased_item[2]} × {list_of_purchased_item[3]}個\n\n'
        purchased_items_info += purchased_item_info

    receipt_contents = f'{time_for_receipt}\n領収書\n\n{purchased_items_info}合計：¥{sum_total_output}\nお預かり：¥{payment_amount}\nお釣り：¥{change}'

    with open(f'./receipt/receipt_{output_receipt_time}.txt', 'w') as f:
        f.write(receipt_contents)

    return f'receipt_{output_receipt_time}.txt'


if __name__ == '__main__':
    main()
