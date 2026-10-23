class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def BstInsertionSequences(root: TreeNode | None) -> list[list[int]]:
    result = []
    path = []

    def visit(available):
        if not available:
            result.append(path.copy())
            return
        for index, node in enumerate(available):
            following = available[:index] + available[index + 1 :]
            if node.Left is not None:
                following.append(node.Left)
            if node.Right is not None:
                following.append(node.Right)
            path.append(node.Data)
            visit(following)
            path.pop()

    visit([root] if root is not None else [])
    return result
