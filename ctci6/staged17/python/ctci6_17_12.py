class BiNode:
    def __init__(self,data: int):
        self.Data=data
        self.Node1: BiNode | None = None
        self.Node2: BiNode | None = None
def ConvertBiNode(root: BiNode | None) -> BiNode | None:
    stack = []
    current = root
    previous = None
    head = None
    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.Node1
        node = stack.pop()
        right = node.Node2
        node.Node1 = previous
        if previous is None:
            head = node
        else:
            previous.Node2 = node
        previous = node
        current = right
    if previous is not None:
        previous.Node2 = None
    return head
