import math
import heapq
from collections import deque

class EmergencyLogistics:
    def __init__(self): 
        self.safety_graph = {
            'KTM': {'JA': 0.90, 'JB': 0.80},
            'JA': {'KTM': 0.90, 'PH': 0.95, 'BS': 0.70},
            'JB': {'KTM': 0.80, 'JA': 0.60, 'BS': 0.90},
            'PH': {'JA': 0.95, 'BS': 0.85},
            'BS': {'JA': 0.70, 'JB': 0.90, 'PH': 0.85}
        }
        
        self.capacity_graph = {
            'KTM': {'JA': 10, 'JB': 15},
            'JA': {'KTM': 10, 'PH': 8, 'BS': 5},
            'JB': {'KTM': 15, 'JA': 4, 'BS': 12},
            'PH': {'JA': 8, 'BS': 6},
            'BS': {'JA': 5, 'JB': 12, 'PH': 6}
        }

    def solve_safest_path(self, start, end):
        print(f"\n{'='*20} STEP 1: SAFEST PATH ANALYSIS {'='*20}")
        print(f"Applying Dijkstra with Log-Transformation: w = -log(p)")
        
        distances = {node: float('inf') for node in self.safety_graph}
        distances[start] = 0
        predecessors = {node: None for node in self.safety_graph}
        pq = [(0, start)]

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if curr_dist > distances[u]: continue

            for v, prob in self.safety_graph[u].items():
                weight = -math.log(prob)
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    heapq.heappush(pq, (distances[v], v))
                    print(f"Relaxing edge {u}->{v}: New Log-Distance = {distances[v]:.4f}")

        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = predecessors[curr]
        
        path = path[::-1]
        actual_safety = math.exp(-distances[end])
        
        print(f"\nRESULT:")
        print(f"Optimal Safest Route: {' -> '.join(path)}")
        print(f"Final Combined Safety Probability: {actual_safety:.4f}")

    def get_max_flow_with_steps(self, source, sink):
        print(f"\n{'='*20} STEP 2: MAX THROUGHPUT (EDMONDS-KARP) {'='*20}")
        residual = {u: dict(neighbors) for u, neighbors in self.capacity_graph.items()}
        total_max_flow = 0
        path_count = 1
        
        while True:
            parent = {source: None}
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for v, cap in residual[u].items():
                    if v not in parent and cap > 0:
                        parent[v] = u
                        queue.append(v)
                if sink in parent: break
            
            if sink not in parent: break 

            path_flow = float('inf')
            temp_path = []
            s = sink
            while s != source:
                temp_path.append(s)
                path_flow = min(path_flow, residual[parent[s]][s])
                s = parent[s]
            temp_path.append(source)
            current_path = " -> ".join(temp_path[::-1])

            print(f"Augmenting Path {path_count}: {current_path} | Flow Added: {path_flow}")
            
            total_max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                residual[u][v] -= path_flow
                if u not in residual[v]: residual[v][u] = 0
                residual[v][u] += path_flow
                v = parent[v]
            
            path_count += 1
                
        print(f"\nFINAL RESULT:")
        print(f"Total Maximum Flow (KTM to BS): {total_max_flow} Trucks/Hour")

if __name__ == "__main__":
    logistics = EmergencyLogistics()
    logistics.solve_safest_path('KTM', 'BS')
    logistics.get_max_flow_with_steps('KTM', 'BS')