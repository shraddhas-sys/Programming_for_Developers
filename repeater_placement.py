import math

def max_repeater_coverage(points):
    n = len(points)
    if n <= 2: return n
    
    max_points = 0
    
    for i in range(n):
        slopes = {}
        duplicate = 1
        current_max = 0
        
        for j in range(i + 1, n):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            
            # Handling overlapping points
            if dx == 0 and dy == 0:
                duplicate += 1
                continue

            common = math.gcd(dx, dy)
            slope = (dx // common, dy // common)
            
            slopes[slope] = slopes.get(slope, 0) + 1
            current_max = max(current_max, slopes[slope])
        
        max_points = max(max_points, current_max + duplicate)
        
    return max_points

customer_locations = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
print(f"Maximum households covered: {max_repeater_coverage(customer_locations)}")