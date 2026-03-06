import math

# Hourly demand 
hourly_demand = {
    6: {'A': 20, 'B': 15, 'C': 25},
    7: {'A': 22, 'B': 16, 'C': 28},
    8: {'A': 24, 'B': 18, 'C': 30}
}

# Energy source constraints
sources = {
    'Solar':  {'capacity': 50, 'available_hours': range(6, 19), 'cost': 1.0},
    'Hydro':  {'capacity': 40, 'available_hours': range(0, 25), 'cost': 1.5},
    'Diesel': {'capacity': 60, 'available_hours': range(17, 24), 'cost': 3.0}
}

tolerance = 0.1

def allocate_energy(hour, demand):
    allocation = {source: {dist: 0 for dist in demand} for source in sources}
    remaining_demand = demand.copy()

    available_sources = {k: v for k, v in sources.items() if hour in v['available_hours']}
    sorted_sources = dict(sorted(available_sources.items(), key=lambda x: x[1]['cost']))

    for src_name, src in sorted_sources.items():
        src_capacity = src['capacity']
        for district, req in remaining_demand.items():
            if req <= 0 or src_capacity <= 0:
                continue

            amount = min(req, src_capacity)
            allocation[src_name][district] = amount
            remaining_demand[district] -= amount
            src_capacity -= amount

    # Check demand
    for district, req_orig in demand.items():
        supplied = sum(allocation[src][district] for src in sources)
        if supplied < req_orig * (1 - tolerance):
            print(f"Warning: Under-supply for {district} at Hour {hour}")

    return allocation

def calculate_total_cost(allocation):
    total = 0
    for src_name, dist_alloc in allocation.items():
        total += sum(dist_alloc.values()) * sources[src_name]['cost']
    return total

# Display results 
results = {}
for hour, demand in hourly_demand.items():
    alloc = allocate_energy(hour, demand)
    cost = calculate_total_cost(alloc)
    
    print(f"\n--- Hour {hour:02d} Results ---")
    print(f"Demand: {demand}")
    for src, dist_vals in alloc.items():
        print(f"  {src:<7}: {dist_vals}")
    print(f"Total Cost: Rs. {cost}")