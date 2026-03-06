class PlantNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class HydropowerOptimizer:
    def __init__(self):
        self.max_generation = float('-inf')

    def calculate_max_power(self, root):
        def dfs(node):
            if not node:
                return 0
            
            left_gain = max(dfs(node.left), 0)
            right_gain = max(dfs(node.right), 0)
            current_path_sum = node.val + left_gain + right_gain
            self.max_generation = max(self.max_generation, current_path_sum)
            return node.val + max(left_gain, right_gain)

        self.max_generation = float('-inf')
        dfs(root)
        return self.max_generation

optimizer = HydropowerOptimizer()

# Basic cascade
ex1_root = PlantNode(1, PlantNode(2), PlantNode(3))
print(f"Example 1 Output: {optimizer.calculate_max_power(ex1_root)}")

# Complex cascade
ex2_root = PlantNode(-10)
ex2_root.left = PlantNode(9)
ex2_root.right = PlantNode(20, PlantNode(15), PlantNode(7))
print(f"Example 2 Output: {optimizer.calculate_max_power(ex2_root)}")