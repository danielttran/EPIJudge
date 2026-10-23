class RandomNode:
    def __init__(self,data: int):
        self.Data=data
        self.Left: RandomNode | None = None
        self.Right: RandomNode | None = None
class RandomSource:
    @staticmethod
    def GetRandom(lower: int,upper: int) -> int:
        return RandomSource.Draw(lower,upper)
class RandomBst:
    class _SizedNode(RandomNode):
        def __init__(self, value: int):
            super().__init__(value)
            self.Size = 1

    def __init__(self):
        self.Root: RandomNode | None = None

    def Insert(self, value: int) -> None:
        added = RandomBst._SizedNode(value)
        if self.Root is None:
            self.Root = added
            return
        path = []
        node = self.Root
        while True:
            path.append(node)
            if value <= node.Data:
                if node.Left is None:
                    node.Left = added
                    break
                node = node.Left
            else:
                if node.Right is None:
                    node.Right = added
                    break
                node = node.Right
        for ancestor in path:
            ancestor.Size += 1

    def Find(self, value: int) -> RandomNode | None:
        node = self.Root
        while node is not None:
            if value == node.Data:
                return node
            node = node.Left if value < node.Data else node.Right
        return None

    def Delete(self, value: int) -> bool:
        path = []
        node = self.Root
        while node is not None and node.Data != value:
            path.append(node)
            node = node.Left if value < node.Data else node.Right
        if node is None:
            return False
        if node.Left is not None and node.Right is not None:
            path.append(node)
            successor = node.Right
            while successor.Left is not None:
                path.append(successor)
                successor = successor.Left
            node.Data = successor.Data
            node = successor
        replacement = node.Left if node.Left is not None else node.Right
        if not path:
            self.Root = replacement
        else:
            parent = path[-1]
            if parent.Left is node:
                parent.Left = replacement
            else:
                parent.Right = replacement
        for ancestor in path:
            ancestor.Size -= 1
        return True

    def GetRandomNode(self) -> RandomNode | None:
        if self.Root is None:
            return None
        rank = RandomSource.GetRandom(0, self.Root.Size - 1)
        node = self.Root
        while node is not None:
            left_size = 0 if node.Left is None else node.Left.Size
            if rank < left_size:
                node = node.Left
            elif rank == left_size:
                return node
            else:
                rank -= left_size + 1
                node = node.Right
        return None
