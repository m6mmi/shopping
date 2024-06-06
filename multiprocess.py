import multiprocessing
import time
import random

import json

import main_functions

products = main_functions.read_products_from_csv('products_2.csv')
# report = {}


# Function for a cashier to serve customers
def cashier_work(cashier_id, customer_queue, served_count, start_event, rest_event, total_served, num_customers, all_customers_served_event, return_dict):
    while not all_customers_served_event.is_set():
        start_event.wait()  # Wait until the start signal is given
        customers_served = 0
        while customers_served < 50 and not all_customers_served_event.is_set():
            if not customer_queue.empty():
                customer = customer_queue.get()
                name = customer['name']
                data = main_functions.process_costumer(products, customer['cart'], customer['card'], f'Cashier_{cashier_id}')
                return_dict[name] = data
                print(f"Cashier {cashier_id} is serving customer {customer}")
                time.sleep(random.uniform(0.1, 0.3))  # Simulate the time taken to serve a customer
                customers_served += 1
                with served_count.get_lock():
                    served_count.value += 1
                with total_served.get_lock():
                    total_served.value += 1

                if total_served.value >= num_customers:
                    all_customers_served_event.set()
                    break
            else:
                time.sleep(0.1)  # Wait for customers to arrive

        print(f"Cashier {cashier_id} is taking a break after serving {customers_served} customers")
        rest_event.set()  # Signal to switch cashiers
        start_event.clear()  # Stop serving more customers
        time.sleep(5)  # Simulate a break


# Function to add customers to the queue
def add_customers(customer_queue, num_customers):
    for i in range(num_customers):
        # customer_queue.put(i + 1)
        customer_queue.put(main_functions.generate_costumer(products, i))
        time.sleep(random.uniform(0.05, 0.2))  # Simulate arrival of customers


# Function to manage cashier start and replacement logic
def manage_cashiers(start_events, rest_events, served_counts, customer_queue, total_served, num_customers, all_customers_served_event):
    while not all_customers_served_event.is_set():
        with served_counts[0].get_lock():
            if served_counts[0].value == 0 and not start_events[0].is_set():
                start_events[0].set()  # Start the first cashier

        if customer_queue.qsize() >= 10 and not start_events[1].is_set():
            start_events[1].set()  # Start the second cashier

        if rest_events[0].is_set():
            start_events[2].set()  # Start the third cashier
            rest_events[0].clear()

        if rest_events[1].is_set():
            start_events[0].set()  # Restart the first cashier
            rest_events[1].clear()

        if rest_events[2].is_set():
            start_events[1].set()  # Restart the second cashier
            rest_events[2].clear()

        time.sleep(0.1)  # Check conditions periodically

    # Stop all cashiers once all customers are served
    for start_event in start_events:
        start_event.set()  # Ensure all cashiers are set to serve so they can exit their loops


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    report = manager.dict()
    num_customers = 200  # Total number of customers
    customer_queue = multiprocessing.Queue()
    served_counts = [multiprocessing.Value('i', 0) for _ in range(3)]
    total_served = multiprocessing.Value('i', 0)
    all_customers_served_event = multiprocessing.Event()

    start_events = [multiprocessing.Event() for _ in range(3)]
    rest_events = [multiprocessing.Event() for _ in range(3)]

    # Create cashier processes
    cashiers = []
    for i in range(3):
        cashier_process = multiprocessing.Process(target=cashier_work, args=(i + 1, customer_queue, served_counts[i], start_events[i], rest_events[i], total_served, num_customers, all_customers_served_event, report))
        cashiers.append(cashier_process)

    # Start cashier processes
    for cashier in cashiers:
        cashier.start()

    # Create and start the manager process
    manager_process = multiprocessing.Process(target=manage_cashiers, args=(start_events, rest_events, served_counts, customer_queue, total_served, num_customers, all_customers_served_event))
    manager_process.start()

    # Add customers to the queue
    add_customers(customer_queue, num_customers)

    # Wait for all customers to be served
    all_customers_served_event.wait()

    # Join cashier and manager processes
    for cashier in cashiers:
        cashier.join()

    manager_process.join()
    with open('multi_report.json', 'w', encoding='utf8') as f:
        json.dump(report.copy(), f, indent=4)
