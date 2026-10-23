class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def IsHeightBalanced(root: TreeNode | None) -> bool:
    if root is None:
        return True
    heights = {}
    stack = [(root, False)]
    while stack:
        node, exiting = stack.pop()
        if not exiting:
            stack.append((node, True))
            if node.Right is not None:
                stack.append((node.Right, False))
            if node.Left is not None:
                stack.append((node.Left, False))
        else:
            left = heights.get(node.Left, 0)
            right = heights.get(node.Right, 0)
            if abs(left - right) > 1:
                return False
            heights[node] = 1 + max(left, right)
    return True
