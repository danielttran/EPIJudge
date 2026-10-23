class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def IsDuplicateLeftBst(root: TreeNode | None) -> bool:
    stack = [(root, -2147483649, 2147483647)] if root is not None else []
    while stack:
        node, lower, upper = stack.pop()
        if node.Data <= lower or node.Data > upper:
            return False
        if node.Right is not None:
            stack.append((node.Right, node.Data, upper))
        if node.Left is not None:
            stack.append((node.Left, lower, node.Data))
    return True
