def get_max_coverage(locations):
    n = len(locations)
    if n <= 2: 
        return n 

    overall_max = 0

    for i in range(n):
        slopes = {}
        for j in range(i + 1, n):
            dx = locations[j][0] - locations[i][0]
            dy = locations[j][1] - locations[i][1]
            
            # String for vertical lines 
            slope = (dy / dx) if dx != 0 else 'inf'
            
            slopes[slope] = slopes.get(slope, 0) + 1
            
        # Update max count 
        if slopes:
            current_max = max(slopes.values()) + 1
            overall_max = max(overall_max, current_max)
            
    return overall_max

# Example test case
customer_locations = [[1,1], [3,2], [5,3], [4,1], [2,3], [1,4]]
result = get_max_coverage(customer_locations)
print(f"Maximum households covered: {result}")