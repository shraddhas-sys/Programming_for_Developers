class TreeNode:
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
            
            left_max = max(dfs(node.left), 0)
            right_max = max(dfs(node.right), 0)
            current_path_sum = node.val + left_max + right_max
            self.max_generation = max(self.max_generation, current_path_sum)
            return node.val + max(left_max, right_max)

        dfs(root)
        return self.max_generation
    
root = TreeNode(-10)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

optimizer = HydropowerOptimizer()
print(f"Maximum Net Power Generation: {optimizer.calculate_max_power(root)}")