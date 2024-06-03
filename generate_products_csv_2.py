import csv
import random

categories = [
    "Electronics", "Home & Garden", "Beauty", "Apparel", "Sports & Outdoors",
    "Tools & Home Improvement", "Home Appliances", "Kitchen & Dining", "Health & Personal Care"
]

product_names = [
    "Samsung Galaxy S21", "Dyson V11 Vacuum", "Olay Regenerist Cream", "Levi's 501 Original Jeans",
    "Nike Air Max 270", "Apple MacBook Pro", "DeWalt Cordless Drill", "Whirlpool Refrigerator",
    "Asus ROG Gaming Laptop", "Instant Pot Duo", "Maybelline Mascara", "Patagonia Down Jacket",
    "Adidas Ultraboost Shoes", "Sony WH-1000XM4 Headphones", "Black+Decker Toaster Oven",
    "Clinique Moisture Surge", "Under Armour Hoodie", "Garmin Forerunner 945", "Philips Sonicare Toothbrush",
    "Trek Marlin 7 Mountain Bike", "Bose QuietComfort 35 II", "Craftsman Tool Set", "KitchenAid Stand Mixer",
    "Neutrogena Hydro Boost Gel", "Columbia Fleece Jacket", "Samsung 65\" QLED TV", "Makita Circular Saw",
    "LG Washing Machine", "MSI Gaming Monitor", "Ninja Blender", "L'Oréal Paris Shampoo",
    "The North Face Parka", "Salomon Trail Running Shoes", "Fitbit Charge 4", "DeLonghi Espresso Machine",
    "Olay Total Effects", "Puma Running Shorts", "Garmin Edge 530", "Oral-B Electric Toothbrush",
    "Huffy Cruiser Bike", "JBL Flip 5 Speaker", "Stanley Tool Box", "Hamilton Beach Coffee Maker",
    "Vichy Mineral 89 Serum", "Reebok Workout Leggings", "Polar H10 Heart Rate Sensor", "Braun Electric Shaver",
    "Keurig Coffee Maker", "Bosch Dishwasher", "Canon EOS Rebel Camera", "Skil Cordless Screwdriver",
    "T-Fal Cookware Set", "Garnier Micellar Water", "Champion Sweatshirt", "Timex Ironman Watch",
    "Phillips Airfryer"
]


def generate_discounts(categories_list):
    categories_dict = {}
    for category in categories_list:
        categories_dict[category] = random.randint(5, 15)

    return categories_dict


def generate_code(codes_generated):
    while True:
        code = random.randint(1000, 9999)
        if code not in codes_generated:
            codes_generated.append(code)
            return code


def generate_product_list(num_products, discounts_dict):
    products = []
    generated_codes = []
    for _ in range(num_products):
        code = generate_code(generated_codes)
        name = random.choice(product_names)
        price = round(random.uniform(5.00, 1500.00), 2)
        category = random.choice(categories)
        discount = discounts_dict[category]
        products.append([code, name, price, category, discount])
    return products


products = generate_product_list(1000, generate_discounts(categories))

with open('products_2.csv', mode='w', newline='', encoding='utf8') as file:
    writer = csv.writer(file)
    writer.writerow(["code", "name", "price", "category", "discount"])
    writer.writerows(products)

print("CSV file 'products.csv' created with 1000 products.")
