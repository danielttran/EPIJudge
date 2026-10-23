class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
class DepthLink:
    def __init__(self, value: TreeNode):
        self.Value = value
        self.Next = None
def LinkedListsByDepth(root: TreeNode | None) -> list[DepthLink]:
    heads = []
    if root is None:
        return heads
    current = [root]
    while current:
        head = tail = None
        following = []
        for node in current:
            link = DepthLink(node)
            if tail is None:
                head = link
            else:
                tail.Next = link
            tail = link
            if node.Left is not None:
                following.append(node.Left)
            if node.Right is not None:
                following.append(node.Right)
        heads.append(head)
        current = following
    return heads
