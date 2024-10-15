import numpy as np

def greedy_capacitated_facility_location(num_clients, num_facilities, opening_costs, service_costs, capacities):
    facility_opened = [False] * num_facilities
    client_assignment = [-1] * num_clients  # -1 means unassigned
    total_cost = 0

    # Keep track of how many clients each facility is serving
    facility_load = [0] * num_facilities

    while True:
        best_cost = float('inf')  # Start with a very high cost
        best_facility = -1

        # Evaluate each facility for opening
        for f in range(num_facilities):
            clients_assigned_f = 0
            if not facility_opened[f]:  # If facility is not already opened
                # Calculate the cost to open this facility and assign clients
                potential_cost = opening_costs[f]

                # Assign clients to the facility if it were opened
                for c in range(num_clients):
                    if client_assignment[c] == -1 and facility_load[f] < capacities[f]:
                        potential_cost += service_costs[f][c]
                        clients_assigned_f += 1

                if potential_cost < best_cost and clients_assigned_f > 0:  # Update best facility to open
                    best_cost = potential_cost
                    best_facility = f

        if best_facility == -1:  # No more facilities can be opened
            break

        # Open the best facility
        facility_opened[best_facility] = True
        total_cost += opening_costs[best_facility]

        # Assign clients to this facility based on service costs
        for c in np.argsort(service_costs[best_facility]):
            if client_assignment[c] == -1 and facility_load[best_facility] < capacities[best_facility]:
                client_assignment[c] = best_facility  # Assign client to this facility
                facility_load[best_facility] += 1  # Increment the load of the facility

    return total_cost, facility_opened, client_assignment

# Create a toy instance
num_clients = 5
num_facilities = 3
opening_costs = [5, 10, 8]  # Costs to open facilities 0, 1, and 2
service_costs = np.array([[2, 4, 1, 3, 5],  # Costs for facility 0 to serve clients 0, 1, 2, 3, 4
                          [3, 1, 2, 4, 6],  # Costs for facility 1 to serve clients 0, 1, 2, 3, 4
                          [4, 3, 2, 1, 7]]) # Costs for facility 2 to serve clients 0, 1, 2, 3, 4
capacities = [2, 2, 3]  # Capacity of facilities 0, 1, and 2

# Running the heuristic on the toy instance
total_cost, facilities_opened, client_assignments = greedy_capacitated_facility_location(
    num_clients, num_facilities, opening_costs, service_costs, capacities)

print("Total cost:", total_cost)
print("Facilities opened:", facilities_opened)
print("Client assignments:", client_assignments)
