import math

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
        
            common = math.gcd(dx, dy)
            slope = (dy // common, dx // common)
            
            slopes[slope] = slopes.get(slope, 0) + 1
            
        if slopes:
            current_max = max(slopes.values()) + 1
            overall_max = max(overall_max, current_max)
            
    return overall_max

example_1_points = [[1,1], [2,2], [3,3]]
print(f"Example 1 Max Coverage: {get_max_coverage(example_1_points)}")