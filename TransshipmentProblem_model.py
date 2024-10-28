import numpy as np
from scipy.optimize import linprog

# Coefficients of the decision variables
C = [1, 2, 6, 3, 2]

# Create constraint matrix
A = np.array([
    [1, 1, 0, 0, 0],
    [-1, 0, 1, 1, 0],
    [0, -1, -1, 0, 1],
    [0, 0, 0, -1, -1],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1]
])

# Right-hand side for the constraints
B = [10, 0, -6, -4, 7, 6, 4, 3, 5]

# Direction of the constraints
constraints_direction = ["="] * 4 + ["<="] * 5

# Find the optimal solution
result = linprog(c=C, A_ub=A, b_ub=B, method='highs')

# Print status: 0 = success, 2 = no feasible solution
print("Status:", result.status)

# Display the optimum values
best_sol = result.x
var_names = ["X12", "X13", "X23", "X24", "X34"]
print("Optimum values:")
for i, name in enumerate(var_names):
    print(f"{name}: {best_sol[i]}")

# Check the value of the objective function at the optimal point
print("Total cost:", result.fun)
