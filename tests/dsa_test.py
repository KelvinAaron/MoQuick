import os
import json
import time
from pathlib import Path
import random

# Load JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "..", "examples", "momo_data.json")

with open(json_path, "r") as f:
    data = json.load(f)

# Making a list
transactions = []
for table in data["momoquick"]:
    for key, tx_list in table.items():
        for tx in tx_list:
            transactions.append(tx)


if len(transactions) < 20:
    print("Warning: Less than 20 transactions available for testing.")

# Prepare a dictionary for O(1) lookup
tx_dict = {tx["Transaction_ID"]: tx for tx in transactions}
 

search_ids = [tx["Transaction_ID"] for tx in random.sample(transactions, min(20, len(transactions)))]

# Linear Search Function
def linear_search(tx_list, tx_id):
    for tx in tx_list:
        if tx.get("Transaction_ID") == tx_id:
            return tx
    return None

# Dictionary Lookup Function
def dict_lookup(tx_dict, tx_id):
    return tx_dict.get(tx_id, None)

# Benchmark Linear Search 
start_linear = time.perf_counter()
for tx_id in search_ids:
    linear_search(transactions, tx_id)
end_linear = time.perf_counter()
linear_time = end_linear - start_linear

# Benchmark Dictionary Lookup
start_dict = time.perf_counter()
for tx_id in search_ids:
    dict_lookup(tx_dict, tx_id)
end_dict = time.perf_counter()
dict_time = end_dict - start_dict

# Print Results
print("DSA Search Benchmark")
print("-------------------")
print(f"Number of records searched: {len(search_ids)}")
print(f"Linear Search Time   : {linear_time:.6f} seconds")
print(f"Dictionary Lookup Time: {dict_time:.6f} seconds")
print(f"Dictionary lookup is {'faster' if dict_time < linear_time else 'slower'} than linear search.")
