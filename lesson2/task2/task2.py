import json

PATH = 'orders.json'


def write_order_to_json(item, quantity, price, buyer, date):
    with open(PATH) as fl:
        data = json.load(fl)

    data['orders'] += ({'item': item,
                        'quantity': quantity,
                        'price': price,
                        'buyer': buyer,
                        'date': date
                        },)

    with open(PATH, 'w') as fl:
        json.dump(data, fl)


write_order_to_json(1, 2, 3, 4, 5)
write_order_to_json(6, 7, 8, 9, 10)
