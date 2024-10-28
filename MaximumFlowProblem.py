import numpy as np
from scipy.optimize import linprog

# Coefficients of the decision variables
C = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Create constraint matrix
A = np.zeros((15, 10))

A[0, 0] = -1
A[0, 1:3] = 1

A[1, 1] = -1
A[1, 3:5] = 1

A[2, 2:4] = -1
A[2, 5:7] = 1

A[3, [4, 5, 8]] = -1
A[3, 7] = 1

A[4, 6] = -1
A[4, 8:10] = 1

A[5, 0] = 1
A[5, [7, 9]] = -1

A[6, 1] = 1
#A[6, 8] = -1

A[7, 2] = 1
A[8, 3] = 1
A[9, 4] = 1
A[10, 5] = 1
A[11, 6] = 1
A[12, 7] = 1
A[13, 9] = 1
A[14, 8] = 1
print(A)

# Direction of the constraints
constraints_direction = ["="] * 6 + ["<="] * 9

# Right-hand side for the constraints
B = [0] * 6 + [6, 8, 3, 3, 4, 2, 2, 8, 6]

# Find the optimal solution
result = linprog(c=-np.array(C), A_ub=A, b_ub=B, bounds=[(0, None)] * 10, method='highs')

# Print status: 0 = success, 2 = no feasible solution
print("Status:", result.success)

# Display the optimum values
best_sol = result.x
var_names = ["V", "XS1", "XS2", "X12", "X13", "X23", "X24", "X3T", "X43", "X4T"]
print("Optimum values:")
for i, name in enumerate(var_names):
    print(f"{name}: {best_sol[i]}")

# Check the value of the objective function at the optimal point
print("Objective function value:", -result.fun)
