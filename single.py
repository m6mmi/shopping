import json
import main_functions

# Read products from CSV
products = main_functions.read_products_from_csv('products_2.csv')
report = {}

if __name__ == "__main__":
    # Adjust the range with number of costumers
    for sequence in range(20):
        costumer = main_functions.generate_costumer(products, sequence)
        main_functions.cashier(report, products, costumer['name'], costumer['cart'], costumer['card'],
                               'Cashier_1')

    with open('single_report.json', 'w', encoding='utf-8') as report_file:
        json.dump(report, report_file, indent=4)
