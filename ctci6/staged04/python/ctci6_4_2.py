class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def CreateMinimalBst(sortedValues: list[int]) -> TreeNode | None:
    def build(lower, upper, parent):
        if lower >= upper:
            return None
        middle = lower + (upper - lower) // 2
        node = TreeNode(sortedValues[middle])
        node.Parent = parent
        node.Left = build(lower, middle, node)
        node.Right = build(middle + 1, upper, node)
        return node

    return build(0, len(sortedValues), None)
