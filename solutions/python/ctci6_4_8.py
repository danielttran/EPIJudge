class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def FirstCommonAncestor(first: TreeNode | None, second: TreeNode | None) -> TreeNode | None:
    if first is None or second is None:
        return None
    depth_first = depth_second = 0
    cursor = first
    while cursor is not None:
        depth_first += 1
        cursor = cursor.Parent
    cursor = second
    while cursor is not None:
        depth_second += 1
        cursor = cursor.Parent
    while depth_first > depth_second:
        first = first.Parent
        depth_first -= 1
    while depth_second > depth_first:
        second = second.Parent
        depth_second -= 1
    while first is not second:
        first = first.Parent
        second = second.Parent
    return first
