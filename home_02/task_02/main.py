import json
from datetime import datetime


def write_order_to_json(item, quantity, price, buyer, date):
    order_dict = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }
    with open('home_02/task_02/orders.json') as js_file:
        temp = json.load(js_file)
    temp['orders'].append(order_dict)    
    with open('home_02/task_02/orders.json', 'w') as js_file:
        json.dump(temp, js_file, indent=4)

        
write_order_to_json("IPhone", 1, 1000, "Alex", str(datetime.now()))