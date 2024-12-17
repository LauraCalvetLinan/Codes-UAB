# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:44:11 2024

@author: 1195147
"""

# SECOND VERSION: One or more products per box
# Define product volumes and box properties
products = [50, 75, 100, 300, 500, 900]
box_types = [
    {"type": "Small", "max_volume": 400, "cost": 6},
    {"type": "Medium", "max_volume": 800, "cost": 8},
    {"type": "Large", "max_volume": 1200, "cost": 9}
]

# Sort products from highest to lowest volume
products.sort(reverse=True)

def pack_products_into_boxes(products, box_types):
    total_cost = 0
    used_boxes = {
        "Small": 0,
        "Medium": 0,
        "Large": 0
    }

    remaining_products = products[:]  # List of unpackaged products
    boxes = []  # List of all used boxes

    while remaining_products:  # Continue while unpackaged products remain
        # Calculate the sum of the sizes of the remaining products
        total_volume = sum(remaining_products)

        # Select the type of box according to the total volume
        if total_volume > box_types[1]["max_volume"]:  # Big box
            box_type = box_types[2]
        elif total_volume > box_types[0]["max_volume"]:  # Medium box
            box_type = box_types[1]
        else:  # Small box
            box_type = box_types[0]

        box = []  # Box to fill
        available_volume = box_type["max_volume"]  # Available volume in the selected box

        # Pack products in the current box
        for product in remaining_products[:]:  # Use a copy to avoid problems when deleting
            if product <= available_volume:
                box.append(product)
                available_volume -= product
                remaining_products.remove(product)  # Remove packaged product

        if box:  # If we have put products in this box, we use it
            used_boxes[box_type["type"]] += 1
            total_cost += box_type["cost"]
            boxes.append(box)

    return used_boxes, total_cost, boxes

# Run the algorithm to package the products
used_boxes, total_cost, packed_boxes = pack_products_into_boxes(products, box_types)

# Print results
print("Boxes used:")
for box_type, count in used_boxes.items():
    print(f"  {box_type} boxes: {count}")
print(f"Total shipping cost: ${total_cost}")

print("Distribution of products in boxes:\n")
for i, box in enumerate(packed_boxes, 1):
    print(f"Box {i}: {box}")
