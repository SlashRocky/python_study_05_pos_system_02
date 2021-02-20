import eel
import desktop
import pos

# インスタンス生成
pos_system = pos.PosSystem()


@eel.expose
def display_inventory():
    return pos_system.display_inventory()


@eel.expose
def register_inventory(product_code, product_name, product_price, product_quantity, product_total):
    return pos_system.register_inventory(product_code, product_name, product_price, product_quantity, product_total)


@eel.expose
def update_inventory(list_of_purchased_items):
    return pos_system.update_inventory(list_of_purchased_items)


@eel.expose
def output_receipt(payment_amount, sum_total_output, change, list_of_purchased_items):
    return pos_system.output_receipt(payment_amount, sum_total_output, change, list_of_purchased_items)


# GUI生成
app_name = "web"
end_point = "index.html"
size = (1020, 1020)
desktop.start(app_name, end_point, size)
