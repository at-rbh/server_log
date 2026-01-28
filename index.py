import time
from datetime import datetime
import csv
import smtplib
from email.message import EmailMessage
from abc import ABC, abstractmethod


def send_email(sender, app_password, receiver, subject, body):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False


# send_email('atiquebd5@gmail.com', 'ygvbxhzsvibkjnen', 'atiiq.liza@gmail.com',
#            "auto email", "message sent via python")

analyze_list = [1, 2, 2, 3, 4, 4, 4]
if analyze_list:

    print(f"Total number of elements: {len(analyze_list)}")

    print(f"Unique elements: {len(set(analyze_list))}")

    frequency_map = {}

    for e in analyze_list:
        frequency_map[e] = frequency_map.get(e, 0) + 1

    print(frequency_map)

    print(f"Unique sum: {sum(set(analyze_list))}")
else:
    print("List is empty")


def clean_password(pwd_list):
    return [
        pwd for pwd in pwd_list
        if len(pwd) >= 8
        and "password" not in pwd.lower()
        and any(ch.isdigit() for ch in pwd)

    ]


print(clean_password(["123666645", "kkkkkkkkkkkkkk", "Secure_88",
      "mypassword99", "short7", "SuperSecret2026"]))

# You have a list of strings representing items and their prices in a messy format: "item_name:price". You need to create a function format_inventory that cleans this up.

# Requirements
# Input: A list of strings like ["apple:1.50", " banana : 2.00 ", "CHERRY: 3"].


def format_inventory(inventory):
    items = {}
    for item in inventory:
        item_name, price = item.split(":")
        price = float(price)
        if price <= 0:
            continue
        items[item_name.strip().lower()] = price

    return items


# Filtering: If a price is less than or equal to 0, exclude it from the result.

# Output: Return a dictionary where the key is the cleaned name and the value is the float price.


# Example Input/Output
products = ["Laptop: 1000", " Mouse:25.50 ", "bad_item:-5", "Keyboard: 50.00"]
# Expected Output: {"laptop": 1000.0, "mouse": 25.5, "keyboard": 50.0}
format_inventory(products)


def process_inventory(data):

    # The Requirements: Write a function process_inventory(data) that takes a list of dictionaries and returns a new dictionary containing:
    low_stock = []
    category = {}
    total = 0
# total_value: The sum of (price×quantity) for all items.
    for k in data:
        total += k["price"] * k["quantity"]
        if k["quantity"] < 10:
            low_stock.append(k["name"])
        category_name = k["category"]
        category[category_name] = category.get(category_name, 0) + 1
    return {
        "Total value": total,
        "Category": category,
        "Low stock": low_stock
    }

# low_stock: A list of names of items where the quantity is less than 10.

# category_count: A dictionary showing how many unique items exist per category.


inventory_data = [
    {"name": "Laptop", "price": 1200, "quantity": 5, "category": "Electronics"},
    {"name": "Mouse", "price": 25, "quantity": 15, "category": "Electronics"},
    {"name": "Desk Chair", "price": 150, "quantity": 8, "category": "Furniture"},
    {"name": "Monitor", "price": 300, "quantity": 12, "category": "Electronics"},
    {"name": "Lamp", "price": 45, "quantity": 3, "category": "Furniture"}
]

print(process_inventory(inventory_data))

# The Requirements: Write a function merge_and_clean_inventories(list_a, list_b) that:

# Merges the two lists.

# Consolidates Duplicates: If an item name exists in both lists (case-insensitive, e.g., "laptop" and "Laptop"), combine them into one entry.

# Sum Quantities: The new quantity should be the sum of both.

# Price Logic: Keep the highest price found for that item.

# Output: Return a list of dictionaries sorted alphabetically by name.


def merge_and_clean_inventories(list_a, list_b):
    merged = {}
    for item in list_a + list_b:
        name = item["name"].lower()
        if name in merged:
            merged[name]["quantity"] += item["quantity"]
            if item["price"] > merged[name]["price"]:
                merged[name]["price"] = item["price"]
        else:
            merged[name] = item.copy()

    return sorted(list(merged.values()), key=lambda x: x["name"])


list_a = [
    {"name": "Laptop", "price": 1000, "quantity": 2},
    {"name": "Mouse", "price": 20, "quantity": 10}
]

list_b = [
    {"name": "laptop", "price": 1100, "quantity": 3},
    {"name": "Keyboard", "price": 50, "quantity": 5}
]

print(merge_and_clean_inventories(list_a, list_b))

# Filters out any dictionary that is missing required keys: "id", "price", and "quantity".

# Validates Types: Ensure price and quantity are numbers (int or float). If they are strings that look like numbers (e.g., "15.50"), convert them. If they aren't numbers, discard the item.

# Handles Negative Values: If a quantity is negative, treat it as 0.

# Formatting: Return a list where each dictionary has a new key "status". If quantity is 0, status is "Out of Stock", otherwise "In Stock".


def clean_api_data(data):
    clean_data = []
    required_keys = ["id", "price", "quantity"]
    for item in data:
        if not all(key in item for key in required_keys):
            continue

        try:
            price = float(item["price"])
            quantity = max(0, int(item["quantity"]))

            cleaned_data = {
                "id": item["id"],
                "price": price,
                "quantity": quantity,
                "status": "Out of Stock" if quantity <= 0 else "In Stock"
            }
            clean_data.append(cleaned_data)
        except ValueError:
            continue
    return clean_data


api_data = [
    {"id": 1, "price": "100", "quantity": 5},      # Valid (convert price)
    {"id": 2, "price": 50},                        # Invalid (missing quantity)
    # Invalid (price not a number)
    {"id": 3, "price": "ten", "quantity": 2},
    {"id": 4, "price": 25, "quantity": -5},        # Valid (convert -5 to 0)
]

print(clean_api_data(api_data))


def calculate_profit_margin(products, sales):
    # Step 1: Create the fast lookup map
    product_map = {p["id"]: p for p in products}

    # Step 2: Dictionary to store profit per product name
    profits_by_name = {}

    for sale in sales:
        p_id = sale["product_id"]

        # Safety check: skip if product ID isn't in our map
        if p_id not in product_map:
            continue

        p_info = product_map[p_id]
        name = p_info["name"]
        cost = p_info["cost"]

        # Calculate profit for THIS specific sale
        sale_profit = sale["amount"] - cost

        # Add to the running total for this product name
        profits_by_name[name] = profits_by_name.get(name, 0) + sale_profit

    return profits_by_name


products = [{"id": 1, "name": "Laptop", "cost": 800}]

sales = [{"product_id": 1, "amount": 1200}, {"product_id": 1, "amount": 1100}]
calculate_profit_margin(products=products, sales=sales)

# catalog: Current products, but some have inconsistent names (casing) and some are missing their base cost.raw_orders: A list of customer orders. Some orders contain multiple items, and some contain "bad data" (negative prices or non-numeric values).
#
# The Requirements:Write a function generate_executive_report(catalog, raw_orders) that:Clean & Map: Create a lookup for the catalog. Normalize names to .title() casing. If a catalog item is missing its "cost", default it to 0.Filter Orders: Ignore any order where the "price" or "quantity" cannot be converted to a number.Calculate Metrics:
print("-" * 30)


def generate_executive_report(catalog, raw_orders):
    catalog_map = {
        p["id"]: {
            "name": p["name"].title(),
            "cost": p.get("cost", 0)
        } for p in catalog
    }
    profit_by_name = {}
    for item in raw_orders:
        try:
            price = float(item["price"])
            quantity = int(item["qty"])

            p_id = item["p_id"]

            if not p_id in catalog_map:
                continue

            product = catalog_map[p_id]
            name = product["name"]
            cost = product["cost"]
            Total_Revenue = price * quantity
            profit = Total_Revenue - (cost * quantity)

            if name not in profit_by_name:
                profit_by_name[name] = {
                    "total_revenue": Total_Revenue, "profit": profit}
            else:
                profit_by_name[name]["total_revenue"] += Total_Revenue
                profit_by_name[name]["profit"] += profit

        except ValueError:
            continue
    return profit_by_name


# For every product, calculate:Total Revenue: (Sum of all price * quantity).Total Profit: (Total Revenue - (Catalog Cost $\times$ Total Quantity Sold)).Final Summary: Return a dictionary where the keys are the Product Names and the values are another dictionary containing the revenue and profit.Efficiency: You must process the catalog once and the orders once. No nested loops.Input Data to Test:
catalog = [
    {"id": "A1", "name": "wireless mouse", "cost": 10},
    {"id": "B2", "name": "MECHANICAL KEYBOARD", "cost": 45},
    {"id": "C3", "name": "Webcam"}  # Missing cost!
]

raw_orders = [
    {"p_id": "A1", "price": "25.0", "qty": 2},     # Valid
    {"p_id": "B2", "price": 100, "qty": 1},        # Valid
    {"p_id": "A1", "price": "20", "qty": "3"},     # Valid
    {"p_id": "C3", "price": "invalid", "qty": 1},  # Skip (Bad price)
    {"p_id": "D4", "price": 50, "qty": 1}          # Skip (Not in catalog)
]

print(generate_executive_report(catalog=catalog, raw_orders=raw_orders))


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.__isbn = isbn
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author}"

    def book_info(self):
        print(f"{self.title.title()} by {self.author}. ISBN: {self.__isbn}")


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_book = list()

    def __str__(self):
        return f"ID: {self.member_id}. Name: {self.name}"

    def borrow_book(self, obj):
        if obj.is_available:
            self.borrowed_book.append(obj)
            obj.is_available = False
            print(f"{obj.title} is borrowed successfully")
        else:
            print(f"{obj.title} is not available")

    def return_book(self, obj):
        if obj in self.borrowed_book:
            self.borrowed_book.remove(obj)
            obj.is_available = True
            print("Book has returned")
        else:
            print(f"Member does not have this book.")


class PremiumMember(Member):
    def __init__(self, member_id, name, max_books):
        super().__init__(member_id, name)
        self.max_books = max_books

    def borrow_book(self, obj):
        if len(self.borrowed_book) >= self.max_books:
            print(f"You have reached maximum limit {self.max_books}.")
        else:
            return super().borrow_book(obj)


book1 = Book("Life of ARB", "ARB", "0123")
book2 = Book("Life of ARB", "liza", "0124")
book3 = Book("Life of ARB", "afifa", "0125")

premium1 = PremiumMember(104, "afifa", 2)
premium1.borrow_book(book1)
premium1.borrow_book(book2)
premium1.borrow_book(book3)


class PaymentMethod:

    @abstractmethod
    def payment_process(self, amount: float):
        pass


class CreditCard(PaymentMethod):

    def payment_process(self, amount):
        total_amount = amount * 1.02
        print(
            f"Processing Credit Card payment of $[{total_amount}] with a 2% transaction fee.")


class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email

    def payment_process(self, amount):
        print(
            f"Processing PayPal payment of $[{amount}] for user [{self.email}].")


class Cryto(PaymentMethod):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    def payment_process(self, amount):
        print(
            f"Processing $[{amount}] via Blockchain. Address: [{self.wallet_address}].")


def execute_checkout(payment_obj: PaymentMethod, amount: float):

    payment_obj.payment_process(amount)


credit_card = CreditCard()

paypal = PayPal("arb@gmail.com")

crypto = Cryto("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa ")

payment_list = [credit_card, paypal, crypto]
for payment in payment_list:
    execute_checkout(payment, 40)


class Light:
    def __init__(self, room_name: str):
        self.room_name = room_name
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print(f"{self.room_name} is on")

    def turn_off(self):
        self.is_on = False
        print("Light is off")


class Thermostat:
    def __init__(self, current_temp):
        self.current_temp = current_temp

    def set_temp(self, new_temp):
        self.current_temp = new_temp


class SmartHome:
    def __init__(self, address: str, lights: list, thermostat: Thermostat):
        self.address = address
        self.lights = lights
        self.thermostat = thermostat

    def add_light(self, light_obj: Light):
        self.lights.append(light_obj)

    def all_lights_on(self):
        for light in self.lights:
            light.turn_on()

    def status(self):
        number_of_light = len(self.lights)
        print(
            f"Address: {self.address}\nTotal light: {number_of_light}\nCurrent temperature: {self.thermostat.current_temp}")


light1 = Light("a1")
light2 = Light("a2")
light3 = Light("a3")

temperature = Thermostat(30)

smart = SmartHome("arb house", [light1, light2, light3], temperature)
smart.add_light(Light("living_room"))
smart.status()
smart.all_lights_on()


class Employee:
    total_employees = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.total_employees += 1

    def emp_info(self):
        return f"Name: {self.name} Salary: {self.salary}"

    @classmethod
    def get_total_employees(cls):
        return cls.total_employees

    @staticmethod
    def is_work_day(day_name):
        return day_name.lower() != "friday"

    @classmethod
    def from_string(cls, data_str):
        name, salary = data_str.split("-")
        return cls(name, int(salary))


# ১. স্ট্যাটিক মেথড কল (অবজেক্ট ছাড়াই সম্ভব)
print(Employee.is_work_day("Friday"))  # Output: False

# ২. ক্লাস মেথড দিয়ে অবজেক্ট তৈরি
emp1 = Employee.from_string("Rahat-60000")

# ৩. মোট এমপ্লয়ী দেখা
print(Employee.get_total_employees())  # Output: 1
print(emp1.emp_info())


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    # এখানে ম্যাজিক মেথডগুলো লিখুন
    def __str__(self):
        return f"Product: {self.name}, Price: {self.price}"

    def __add__(self, other):
        return self.price + other.price

    def __gt__(self, other):
        return self.price > other.price


# --- টেস্ট করার জন্য ---
p1 = Product("Laptop", 50000)
p2 = Product("Mouse", 1500)

print(p1)          # আউটপুট হওয়া উচিত: Product: Laptop, Price: 50000
print(p1 + p2)     # আউটপুট হওয়া উচিত: 51500 (দুটি দামের যোগফল)
print(p1 > p2)     # আউটপুট হওয়া উচিত: True


class BankAccount:
    def __init__(self):
        self.__balance = 0  # প্রাইভেট অ্যাট্রিবিউট

    # এখানে @property ব্যবহার করে গেটার লিখুন
    @property
    def balance(self):
        return self.__balance

    # এখানে @balance.setter ব্যবহার করে সেটার লিখুন
    @balance.setter
    def balance(self, new_amount):
        if new_amount < 0:
            raise ValueError("Amount can not be less then zero")
        self.__balance = new_amount


# --- টেস্ট করার জন্য ---
acc = BankAccount()

acc.balance = 500   # এটি সেটারকে কল করবে এবং ব্যালেন্স ৫০০ করবে
print(acc.balance)  # এটি গেটারকে কল করবে

try:
    acc.balance = -100  # এটি একটি এরর মেসেজ দিবে
except ValueError as e:
    print(e)
print(acc.balance)  # ব্যালেন্স আগের মতোই ৫০০ থাকবে


class MenuItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.__price = price

    def __str__(self):
        return f"{self.name} price: {self.__price}"

    @property
    def item_price(self):
        return self.__price

    @item_price.setter
    def item_price(self, new_price):
        if new_price < 0:
            raise ValueError("Price can't be zero")
        self.__price = new_price

    def __add__(self, other):
        return self.item_price + other.item_price


class Order:
    def __init__(self):
        self.items = []

    def __str__(self):
        return f"{self.items}"

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.item_price for item in self.items)


class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass


class CashPayment(Payment):
    def pay(self, amount: float):
        print(f"Payment process ${amount}")
        return amount


class CardPayment(Payment):
    def pay(self, amount: float):
        print(f"Payment process ${amount * 1.02}")
        return amount


class Manager:
    total_revenue = 0

    @classmethod
    def update_revenue(cls, amount):
        cls.total_revenue += amount

    @staticmethod
    def is_open(day):
        return day.lower() != "friday"


burger = MenuItem("Burger", 30)
pizza = MenuItem("Pizza", 20)
order = Order()
order.add_item(burger)
order.add_item(pizza)

cash_payment = CashPayment()
card_payment = CardPayment()

total_amount = order.calculate_total()
cash_payment.pay(total_amount)
card_payment.pay(total_amount)

manager = Manager()
manager.update_revenue(total_amount)
print(manager.total_revenue)


# def read_inventory():
#     try:
#         with open("inventory.csv", "r") as file:
#             reader = csv.DictReader(file)
#             return list(reader)

#     except FileNotFoundError:
#         print("File not found")


# def inventory(data):
#     return {
#         row["item_id"]: {
#             "name": row["item_name"],
#             "category": row["category"],
#             "price": float(row["price"]),
#             "quantity": int(row["quantity"])

#         } for row in data
#     }


# def stock_update(data, item_id, change_qty):
#     if item_id not in data:
#         raise KeyError("Item not found")

#     current_qty = data[item_id]["quantity"]
#     new_qty = current_qty + change_qty

#     data[item_id]["quantity"] = max(0, new_qty)

#     return data[item_id]["quantity"]


# def lowest_stock(data):
#     return [{item["name"]: item["quantity"] for item in data.values() if item["quantity"] <= 5}]


# def inventory_summary(inventory_data):
#     summary = {}

#     for item in inventory_data.values():
#         category = item["category"]
#         total_price = item["price"] * item["quantity"]
#         if category not in summary:
#             summary[category] = {"total_items": 1,
#                                  "total_value": total_price}
#         else:
#             summary[category]["total_items"] += 1
#             summary[category]["total_value"] += total_price
#     return summary


# def search_by_name(item_name, inventory_list):
#     for item in inventory_list.values():
#         if item["name"].lower() == item_name.lower():
#             print("Item found")
#             return item
#     print("Item not found")


# def print_summary(summary):
#     print(f"{'Category':<15} | {'Count':<10} | {'Total Value':<15}")
#     print("*" * 45)
#     for cat, stat in summary.items():
#         print(
#             f"{cat:<15} | {stat['total_items']:<10} | {stat['total_value']:<15}")


# def save_update_csv(update_stock, filename):
#     fieldnames = ["item_id", "item_name", "category", "price", "quantity"]

#     with open(filename, "w", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)

#         writer.writeheader()

#         for item_id, details in update_stock.items():
#             writer.writerow({
#                 "item_id": item_id,
#                 "item_name": details["name"],
#                 "category": details["category"],
#                 "price": details["price"],
#                 "quantity": details["quantity"]
#             })
#     print("Updated file successfully")


# raw_data = read_inventory()

# inventory_list = inventory(raw_data)

# stock_update(inventory_list, "I101", 20)
# lowest_stock(inventory_list)
# summary = inventory_summary(inventory_list)
# search_by_name("Keyboard", inventory_list)
# print_summary(summary)
# save_update_csv(inventory_list, "updated_csv.csv")
def server_log(filename):
    try:
        with open(filename, "r") as file:
            data = [line.strip() for line in file.readlines()]
            return data
    except FileNotFoundError:
        print("File not found")
        return []


def log_count(server_data):
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for line in server_data:
        parts = line.split()
        if len(parts) >= 3:
            level = parts[2]
            if level in line:
                counts[level] += 1
    return counts


def frequency(server_data):
    freq = {}
    for line in server_data:
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) > 2:
            level = line.split()[2]
            if level == "ERROR":
                message = line.split(level, 1)[1].strip()
                if message not in freq:
                    freq[message] = 1
                else:
                    freq[message] += 1
    return freq


def error_peak_hour(server_data):
    error_count = {}

    for line in server_data:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) > 1:
            level = line.split()[2]
            if level == "ERROR":
                log_time = line.split()[1]

                dt = datetime.strptime(log_time, "%H:%M:%S")
                hour = dt.hour
                error_count[hour] = error_count.get(
                    hour, 0) + 1
    max_hours = max(error_count, key=error_count.get)
    return {
        f"{max_hours}:00 - {max_hours}:59": error_count[max_hours]
    }


def save_file(log, freq, error):
    with open("server.txt", "w") as file:
        file.write("All log file count\n")
        for message, count in log.items():
            file.write(f"{message}: {count}\n")

        file.write("\nfrequency error data\n")
        for message, count in freq.items():

            file.write(f"{message}: {count}\n")

        file.write("\nError peak hour\n")
        for time, count in error.items():
            file.write(f"{time}: {count}\n")


raw_data = server_log("server.log")
log = log_count(raw_data)
freq = frequency(raw_data)
error = error_peak_hour(raw_data)
save_file(log, freq, error)
