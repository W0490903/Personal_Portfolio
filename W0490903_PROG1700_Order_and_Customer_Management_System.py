"""
Author: Zachary Mason
Student ID: W0490903
Course: PROG1700
Date: 2023-12-06
Project: Order and Customer Management System Using Sets, Lists, and Dictionaries.
Repository: https://github.com/W0490903/PROG1700/
Programming Language: Python 3
"""

customers = {
    1:{'name': 'Zachary', 'contact': '12345', 'orders': [{'order_id': 1, 'product_name': 'Bananas', 'quantity': 2, 'total_cost': 46.0}]},
    2:{'name': 'Alice', 'contact': '12346', 'orders': [{'order_id': 1, 'product_name': 'Bananas', 'quantity': 2, 'total_cost': 46.0}]}
}

def add_customer():
    while True:
        new_customer_name = input("Please enter name for new customer: ").strip().title()

        if any(customer_info['name'] == new_customer_name for customer_info in customers.values()):
            print('Customer already exists! Please enter a different name.')
        else:
            contact = input("Please enter new customer's contact number (XXX-XXX-XXXX): ").strip()
            orders = []
            new_customer_id = max(customers.keys(), default=0) + 1

            customers[new_customer_id] = {
                'name': new_customer_name,
                'contact': contact,
                'orders': orders
            }
            print("Customer added successfully!")
            break

def place_order():
    while True:
        for customer_id, customer_details in customers.items():
            print(f"{customer_id}: {customer_details['name']}")
        
        customer_search = input("Please select ID of customer to add order: ").strip()
        
        try:
            customer_search = int(customer_search)
        except ValueError:
            print("Error! Please select using a number ID only!")
            continue
        
        if customer_search not in customers.keys():
            print("You have selected an invalid ID number!")
        else:
           product_name = input("Product Name: ").strip().title()
           product_quantity = int(input("Quantity: ").strip())
           product_cost = float(input("Total Cost: ").strip())
           
           new_order = {
               'order_id': len(customers[customer_search]['orders']) + 1,
               'product_name': product_name,
               'quantity': product_quantity,
               'total_cost': product_cost 
            }
           
           customers[customer_search]['orders'].append(new_order)
           print("Order placed successfully!")
           break

def generate_customer_report():
    while True:
        for customer_id, customer_details in customers.items():
            print(f"{customer_id}: {customer_details['name']}")
        
        customer_search = input("Please select a customer ID to generate a report: ").strip()

        try:
            customer_search = int(customer_search)
        except ValueError:
            print("Error! Please select using a number ID only!")
            continue

        if customer_search not in customers.keys():
            print("You have selected an invalid ID number!")
        else:
            customer_report = customers[customer_search]
            print("\nCustomer Report:")
            print(f"ID: {customer_search}")
            print(f"Name: {customer_report['name']}")
            print(f"Contact: {customer_report['contact']}")

            if customer_report['orders']:
                print("\nOrders:\n--------------------")
                for order in customer_report['orders']:
                    print(f"Order ID: {order['order_id']}")
                    print(f"Product Name: {order['product_name']}")
                    print(f"Quantity: {order['quantity']}")
                    print(f"Total Cost: {order['total_cost']}\n")
            else:
                print("There are no orders found for this customer!")
  
def generate_customer_report_all():
    for customer_id , customer_details in customers.items():
        print("\nCustomer Report:")
        print(f"ID: {customer_id}")
        print(f"Name: {customer_details['name']}")
        print(f"Contact: {customer_details['contact']}")

        if customer_details['orders']:
            print("\nOrders:\n--------------------")
            for order in customer_details['orders']:
                print(f"Order ID: {order['order_id']}")
                print(f"Product Name: {order['product_name']}")
                print(f"Quantity: {order['quantity']}")
                print(f"Total Cost: {order['total_cost']}\n")
        else:
            print("There are no orders found for this customer!")

# Main Menu
while True:
    selection = input(
"""\nOrder and Customer Management System:
[1] Add Customer
[2] Place Order
[3] Generate Customer Report
[4] Generate All Customer Reports
[5] Exit\n
Please make a selection (1-5): """)
    
    if not selection.isdigit():
        print("Please make a valid selection! (1-5)")
        continue
    
    selection = int(selection)

    if selection < 1 or selection > 6:
        print("\nPlease make a valid selection! (1-5)")
    elif selection == 1:
        add_customer()
    elif selection == 2:
        place_order()
        print(customers)
    elif selection == 3:
        generate_customer_report()
    elif selection == 4:
        generate_customer_report_all()
    elif selection == 5:
        exit()