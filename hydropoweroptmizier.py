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
            
            # 1. Get max power from left and right (ignore if negative)
            left_max = max(dfs(node.left), 0)
            right_max = max(dfs(node.right), 0)
            
            # 2. Potential max path passing through this node
            current_path_sum = node.val + left_max + right_max
            
            # 3. Update global maximum
            self.max_generation = max(self.max_generation, current_path_sum)
            
            # 4. Return the maximum "single branch" to the parent
            return node.val + max(left_max, right_max)

        dfs(root)
        return self.max_generation

# Testing with Example 2
# root = -10, left = 9, right = 20 (left=15, right=7)
root = TreeNode(-10)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

optimizer = HydropowerOptimizer()
print(f"Maximum Net Power Generation: {optimizer.calculate_max_power(root)}")