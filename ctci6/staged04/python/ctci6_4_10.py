class TreeNode:
    def __init__(self, data: int):
        self.Data = data
        self.Left = self.Right = self.Parent = None
def ContainsExactSubtree(large: TreeNode | None, small: TreeNode | None) -> bool:
    if small is None:
        return True

    def encode(root):
        tokens = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                tokens.append("#")
            else:
                tokens.append("V" + str(node.Data))
                stack.append(node.Right)
                stack.append(node.Left)
        return tokens

    text, pattern = encode(large), encode(small)
    prefix = [0] * len(pattern)
    for index in range(1, len(pattern)):
        matched = prefix[index - 1]
        while matched and pattern[index] != pattern[matched]:
            matched = prefix[matched - 1]
        if pattern[index] == pattern[matched]:
            matched += 1
        prefix[index] = matched
    matched = 0
    for token in text:
        while matched and token != pattern[matched]:
            matched = prefix[matched - 1]
        if token == pattern[matched]:
            matched += 1
        if matched == len(pattern):
            return True
    return False
