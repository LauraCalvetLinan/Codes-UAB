import random

## Parameters of the problem
num_workers = 10
total_days = 120
requested_rest_days = 10  # Number of days workers have to rest
max_workers_per_day = 2  # Maximum workers allowed to rest per day

## Requests for each worker
workers_requested_rest = {i: random.sample(range(total_days), requested_rest_days) for i in range(num_workers)}
print(workers_requested_rest)

## Generate initial schedule
def generate_initial_schedule():
    initial_schedule = [[] for _ in range(total_days)]
    worker_rest_counts = {i: 0 for i in range(num_workers)}

    for worker in range(num_workers):
        rest_days = workers_requested_rest[worker]
        random.shuffle(rest_days)

        for day in rest_days:
            if worker_rest_counts[worker] < 10 and len(initial_schedule[day]) < max_workers_per_day:
                initial_schedule[day].append(worker)
                worker_rest_counts[worker] += 1

    return initial_schedule

## Evaluate a given schedule
def evaluate_schedule(schedule):
    # Calculate the number of approved rest days
    approved_rest_days = 0
    for worker in range(num_workers):
        for requested_day in workers_requested_rest[worker]:
            if worker in schedule[requested_day]:
                approved_rest_days += 1

    return approved_rest_days

## Multi-start heuristic (main solving approach)
def multi_start_heuristic(num_iterations):
    best_schedule = generate_initial_schedule()
    best_score = evaluate_schedule(best_schedule)

    for _ in range(num_iterations):
        new_schedule = generate_initial_schedule()
        new_score = evaluate_schedule(new_schedule)

        if new_score > best_score:
            best_schedule = new_schedule
            best_score = new_score

    return best_schedule, best_score

## Parameter of the algorithm
num_iterations = 1000 # Define the number of iterations

best_schedule, best_score = multi_start_heuristic(num_iterations)

# Display solutions
print("Best Schedule:")
for day, workers in enumerate(best_schedule):
    print(f"Day {day}: Workers resting - {workers}")
print(f"Total Approved Rest Days: {best_score}")