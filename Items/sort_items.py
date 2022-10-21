with open('Items/items.txt', 'r') as f:
    items = f.readlines()

all_items = []

for item in items:
    if item not in all_items:
        all_items.append(item)

with open('Items/items.txt', 'w') as f:
    f.writelines(all_items)
