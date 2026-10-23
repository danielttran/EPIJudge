class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def CountDownwardSumPaths(root: TreeNode | None, target: int) -> int:
    if root is None:
        return 0
    prefix = {0: 1}
    stack = [(root, 0, False)]
    answer = 0
    while stack:
        node, running, exiting = stack.pop()
        if exiting:
            prefix[running] -= 1
            if prefix[running] == 0:
                del prefix[running]
            continue
        running += node.Data
        answer += prefix.get(running - target, 0)
        prefix[running] = prefix.get(running, 0) + 1
        stack.append((node, running, True))
        if node.Right is not None:
            stack.append((node.Right, running, False))
        if node.Left is not None:
            stack.append((node.Left, running, False))
    return answer
