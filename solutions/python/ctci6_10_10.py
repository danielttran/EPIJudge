class RankTracker:
    class _Node:
        def __init__(self, value):
            self.value = value
            self.left_count = 0
            self.left = self.right = None

    def __init__(self):
        self._root = None

    def Track(self, value: int) -> None:
        if self._root is None:
            self._root = self._Node(value)
            return
        node = self._root
        while True:
            if value <= node.value:
                node.left_count += 1
                if node.left is None:
                    node.left = self._Node(value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = self._Node(value)
                    return
                node = node.right

    def GetRank(self, value: int) -> int:
        node = self._root
        skipped = 0
        while node is not None:
            if value == node.value:
                return skipped + node.left_count
            if value < node.value:
                node = node.left
            else:
                skipped += node.left_count + 1
                node = node.right
        return -1
