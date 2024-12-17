# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:39:36 2024

@author: 1195147
"""

# FIRST VERSION: One product per box
# Define product volumes and box properties
products = [50, 75, 100, 300, 500, 900]
box_types = [
    {"type": "Small", "max_volume": 400, "cost": 6},
    {"type": "Medium", "max_volume": 800, "cost": 8},
    {"type": "Large", "max_volume": 1200, "cost": 9}
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
    total_cost += box_types[2]["cost"]
# Output results
print(f"Small boxes used: {small_boxes}")
print(f"Medium boxes used: {medium_boxes}")
print(f"Large boxes used: {large_boxes}")
print(f"Total shipping cost: ${total_cost}")
