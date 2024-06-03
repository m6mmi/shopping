import csv
import random
from faker import Faker
from collections import deque


class Product:
    def __init__(self, code, name, price, category, discount):
        self.category = category
        self.code = code
        self.name = name
        self.price = price
        self.discount = discount

    def __repr__(self):
        return (f"Product(code={self.code}, name={self.name}, price={self.price:.2f}, category={self.category},"
                f"discount={self.discount}, discount price={(100 - self.discount) * self.price / 100:.2f}")


def read_products_from_csv(filepath):
    products = {}
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            code = int(row['code'])
            name = row['name']
            price = float(row['price'])
            category = row['category']
            discount = int(row['discount'])
            product = Product(code, name, price, category, discount)
            products[code] = product
    return products


def generate_costumer(product_list, que_nr):
    costumer_data = {}
    shopping_cart = random.sample(sorted(product_list.keys()), random.randint(1, 10))
    loyalty_card = random.choice([True, False])
    costumer_data['name'] = f'Costumer_{que_nr + 1}'
    costumer_data['cart'] = shopping_cart
    costumer_data['card'] = loyalty_card

    return costumer_data


def generate_costumer_list(product_list, nr_of_costumers):
    costumers_list = deque()
    for costumer in range(nr_of_costumers):
        costumer_data = {}
        name = Faker().name()
        shopping_cart = random.sample(sorted(product_list.keys()), random.randint(1, 10))
        loyalty_card = random.choice([True, False])
        costumer_data['name'] = name
        costumer_data['cart'] = shopping_cart
        costumer_data['card'] = loyalty_card
        costumers_list.append(costumer_data)

    return costumers_list


def process_costumer(product_list, shopping_cart, loyalty_card, cashier):
    costumer = {}
    cart = []
    total = 0
    total_discount = 0
    for product_code in shopping_cart:
        # print(product_list[product_code])
        product_name = product_list[product_code].name
        price = product_list[product_code].price
        discount_price = round(price * (100 - product_list[product_code].discount) / 100, 2)
        total += price
        total_discount += discount_price
        if loyalty_card is True:
            cart.append({'product': product_name, 'price': price, 'loyalty_price': discount_price})
        else:
            cart.append({'product': product_name, 'price': price})

    costumer['shopping_cart'] = cart
    costumer['total'] = round(total, 2)
    if loyalty_card is True:
        costumer['loyalty_total'] = round(total_discount, 2)
    costumer['cashier'] = cashier

    return costumer


def cashier(report_dict, products_list, name, cart, card, cashier_name):
    data = process_costumer(products_list, cart, card, cashier_name)
    print(f'{cashier_name} processed costumer: name = {name}, shopping cart = {cart}, loyalty card = {card}')
    report_dict[name] = data
