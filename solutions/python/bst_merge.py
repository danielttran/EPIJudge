from bst_node import BstNode

def merge_two_bsts(first, second):
    def inorder(node):
        values, stack = [], []
        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            values.append(node.data)
            node = node.right
        return values
    a, b = inorder(first), inorder(second)
    merged = []
    i = j = 0
    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    def build(start, end):
        if start == end:
            return None
        middle = start + (end - start) // 2
        return BstNode(merged[middle], build(start, middle), build(middle + 1, end))
    return build(0, len(merged))
