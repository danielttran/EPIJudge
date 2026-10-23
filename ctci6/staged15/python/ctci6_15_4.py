class ResourceLock:
    def Lock(self) -> None:
        raise RuntimeError("Provided native resource lock")
    def Unlock(self) -> None:
        raise RuntimeError("Provided native resource lock")
class LockPool:
    def Get(self,resource: int) -> ResourceLock:
        raise RuntimeError("Provided stable native lock pool")
class DeadlockFreeLocks:
    def __init__(self, resourceCount: int, pool: LockPool):
        self._count = resourceCount
        self._pool = pool
        self._orders = [[] for _ in range(4)]
        self._next = [0] * 4

    def Declare(self, owner: int, order: list[int]) -> bool:
        if not 0 <= owner < 4:
            return False
        seen = [False] * self._count
        for resource in order:
            if not 0 <= resource < self._count or seen[resource]:
                return False
            seen[resource] = True
        reach = [[False] * self._count for _ in range(self._count)]
        for candidate in range(4):
            path = order if candidate == owner else self._orders[candidate]
            for first, second in zip(path, path[1:]):
                reach[first][second] = True
        for middle in range(self._count):
            for first in range(self._count):
                for second in range(self._count):
                    reach[first][second] |= reach[first][middle] and reach[middle][second]
        if any(reach[i][i] for i in range(self._count)):
            return False
        self._orders[owner] = order.copy()
        self._next[owner] = 0
        return True

    def GetLock(self, owner: int, resource: int) -> ResourceLock | None:
        if not 0 <= owner < 4:
            return None
        path = self._orders[owner]
        position = self._next[owner]
        if position == len(path) or path[position] != resource:
            return None
        self._next[owner] += 1
        return self._pool.Get(resource)
