import pandas as pd
import random
from datetime import datetime, timedelta

# Function to generate a random date between two dates
def random_date(start, end):
    return start + (end - start) * random.random()

# Function to generate a large amount from one account split into smaller similar amounts
def generate_large_split_transactions(base_amount, num_splits):
    transactions = []
    source_id = random.randint(1, 1000)
    for _ in range(num_splits):
        # Introduce a small random variation
        variation = random.uniform(-0.05, 0.05) * base_amount / num_splits
        amount = round(base_amount / num_splits + variation, 2)
        transactions.append({
            "typeofaction": "transfer",
            "sourceid": source_id,
            "destinationid": random.randint(1, 1000),
            "amountofmoney": amount,
            "date": random_date(datetime(2020, 1, 1), datetime(2024, 12, 31)).strftime('%Y-%m-%d %H:%M'),
            "isfraud": 1,
            "typeoffraud": "type1"
        })
    return transactions

# Function to generate sequential transfers with similar but varied amounts
def generate_sequential_transfers(num_transfers):
    transactions = []
    date = random_date(datetime(2020, 1, 1), datetime(2024, 12, 31))
    base_amount = random.uniform(10, 1000)
    for i in range(num_transfers):
        # Introduce a small random variation
        variation = random.uniform(-0.05, 0.05) * base_amount
        amount = round(base_amount + variation, 2)
        transactions.append({
            "typeofaction": "transfer",
            "sourceid": random.randint(1, 1000),
            "destinationid": random.randint(1, 1000),
            "amountofmoney": amount,
            "date": (date + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M'),
            "isfraud": 1,
            "typeoffraud": "type2"
        })
    return transactions

# Function to generate multiple small transfers to one person with varied amounts
def generate_small_to_large_transfers(num_transfers, total_amount):
    transactions = []
    recipient_id = random.randint(1, 1000)
    base_amount = total_amount / num_transfers
    for _ in range(num_transfers):
        # Introduce a small random variation
        variation = random.uniform(-0.05, 0.05) * base_amount
        amount = round(base_amount + variation, 2)
        transactions.append({
            "typeofaction": "transfer",
            "sourceid": random.randint(1, 1000),
            "destinationid": recipient_id,
            "amountofmoney": amount,
            "date": random_date(datetime(2020, 1, 1), datetime(2024, 12, 31)).strftime('%Y-%m-%d %H:%M'),
            "isfraud": 1,
            "typeoffraud": "type3"
        })
    return transactions

# Function to generate random non-fraudulent transactions
def generate_random_transaction():
    transaction_types = ["cash-in", "transfer"]
    action = random.choice(transaction_types)
    amount = round(random.uniform(10, 10000), 2)
    return {
        "typeofaction": action,
        "sourceid": random.randint(1, 1000),
        "destinationid": random.randint(1, 1000),
        "amountofmoney": amount,
        "date": random_date(datetime(2020, 1, 1), datetime(2024, 12, 31)).strftime('%Y-%m-%d %H:%M'),
        "isfraud": 0,
        "typeoffraud": "none"
    }

# Generate a list of transactions
transactions = []

# Generate transactions based on rules
for _ in range(500):
    transactions.extend(generate_large_split_transactions(100000, 5))
    transactions.extend(generate_sequential_transfers(5))
    transactions.extend(generate_small_to_large_transfers(5, 100000))
    for _ in range(15):
        transactions.append(generate_random_transaction())

# Create a DataFrame
df = pd.DataFrame(transactions)

# Save to CSV
df.to_csv("generated_transactions.csv", index=False)

print("CSV file with generated transactions created successfully.")
