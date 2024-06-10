from time import perf_counter_ns

items = [
    {"name": "Laptop", "category": "Electronics"},
    {"name": "Headphones", "category": "Electronics"},
    {"name": "Camera", "category": "Electronics"},
    {"name": "Books", "category": "Books"},
    {"name": "Shoes", "category": "Clothing"},
    {"name": "Clothing", "category": "Clothing"},
    {"name": "Kitchen Appliances", "category": "Home & Kitchen"},
    {"name": "Furniture", "category": "Home & Kitchen"},
    {"name": "Toys", "category": "Toys & Games"},
    {"name": "Fitness Equipment", "category": "Sports & Outdoors"},
    {"name": "Beauty Products", "category": "Beauty"},
    {"name": "Gaming Consoles", "category": "Electronics"},
    {"name": "Outdoor Gear", "category": "Sports & Outdoors"},
    {"name": "Home Decor", "category": "Home & Kitchen"},
    {"name": "Smartphone", "category": "Electronics"}
]

def linear_search(data, target):
    for index, item in enumerate(data):
        if item['name'] == target:
            return index
    return -1

def heuristic_linear_search(data, target):
    for index, item in enumerate(data):
        if item['name'] == target:
            # Move the found item to the front of the list
            data.insert(0, data.pop(index))
            return index
    return -1

def categorize_items(items):
    categories = {}
    for item in items:
        category = item['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    return categories

item = "Smartphone"
time = 0

# Using linear search
start_time = perf_counter_ns()
index = linear_search(items, item)
end_time = perf_counter_ns()
time = end_time - start_time
print(f"Time taken for linear search: {time} nanoseconds")
print(f"Linear search: {item} found at index {index}")
print("-" * 30)

# Heuristic linear search the item that is at the end of the list
index = heuristic_linear_search(items, item)
time = end_time - start_time

# Using heuristic linear search with item after moving to front
start_time = perf_counter_ns()
index = heuristic_linear_search(items, item)
end_time = perf_counter_ns()
time = end_time - start_time
print(f"Time taken for heuristic optimized: {time} nanoseconds")
print(f"Heuristic linear search: {item} found at index {index}")
print("-" * 30)

# Categorize items
categories = categorize_items(items)

# Search within a category
category = "Electronics"

# Using linear search
start_time = perf_counter_ns()
index = linear_search(categories[category], item)
end_time = perf_counter_ns()
time = end_time - start_time
print(f"Time taken for linear search within {category}: {time} nanoseconds")
print(f"Linear search within {category}: {item} found at index {index}")