class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def InorderSuccessor(node: TreeNode | None) -> TreeNode | None:
    if node is None:
        return None
    if node.Right is not None:
        following = node.Right
        while following.Left is not None:
            following = following.Left
        return following
    current, parent = node, node.Parent
    while parent is not None and current is parent.Right:
        current, parent = parent, parent.Parent
    return parent
