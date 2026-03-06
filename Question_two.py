class PlantNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_power_generation(root):
    max_generation = float('-inf')

    def calculate_gain(node):
        nonlocal max_generation
        if not node:
            return 0
        
        left_gain = max(calculate_gain(node.left), 0)
        right_gain = max(calculate_gain(node.right), 0)

        current_path_sum = node.val + left_gain + right_gain
        max_generation = max(max_generation, current_path_sum)
        return node.val + max(left_gain, right_gain)

    calculate_gain(root)
    return max_generation

root_ex2 = PlantNode(-10)
root_ex2.left = PlantNode(9)
root_ex2.right = PlantNode(20)
root_ex2.right.left = PlantNode(15)
root_ex2.right.right = PlantNode(7)

print(f"Maximum net power generation: {max_power_generation(root_ex2)}")