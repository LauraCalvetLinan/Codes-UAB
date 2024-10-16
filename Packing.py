# FIRST VERSION: One product per box
x_list = [200,180,300,300,190,200,210,220,230,190]
y_list = [5,6,5,3,4,5,6,7,8,7]
z_list = [1200,1200,1000,1000,1100,1000,1100,1000,1100,1200]

i = 9
x = x_list[i]
y = y_list[i]
z = z_list[i]

# Define product volumes and box properties
products = [50, 75, 100, x, 300, 400]
box_types = [
    {"type": "Small", "max_volume": 400, "cost": y},
    {"type": "Medium", "max_volume": 800, "cost": 8},
    {"type": "Large", "max_volume": z, "cost": 9}
]
# Initialize counters for the number of each type of box
small_boxes = 0
medium_boxes = 0
large_boxes = 0
total_cost = 0
# Packing logic
for product in products:
  if product <= box_types[0]["max_volume"]:
    small_boxes += 1
    total_cost += box_types[0]["cost"]
  elif product <= box_types[1]["max_volume"]:
    medium_boxes += 1
    total_cost += box_types[1]["cost"]
  else:
    large_boxes += 1
    total_cost += box_types[2]["max_volume"]
# Output results
print(f"Small boxes used: {small_boxes}")
print(f"Medium boxes used: {medium_boxes}")
print(f"Large boxes used: {large_boxes}")
print(f"Total shipping cost: ${total_cost}")

# SECOND VERSION: One or more products per box
# Sort products from highest to lowest volume
products.sort(reverse=True)

def pack_products_into_boxes(products, box_types):
    """Función para empaquetar productos en cajas de diferentes tipos minimizando el costo."""
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
        if total_volume > box_types[2]["max_volume"]:  # Big box
            box_type = box_types[2]
        elif total_volume > box_types[1]["max_volume"]:  # Medium box
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
print("Cajas usadas:")
for box_type, count in used_boxes.items():
    print(f"  {box_type} boxes: {count}")
print(f"Total shipping cost: ${total_cost}")

print("Distribution of products in boxes\n:")
for i, box in enumerate(packed_boxes, 1):
    print(f"Box {i}: {box}")
