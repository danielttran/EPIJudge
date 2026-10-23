def SmallestK(values: list[int], k: int) -> list[int]:
    if k == 0:
        return []
    import heapq

    heap = [-values[i] for i in range(k)]
    heapq.heapify(heap)
    for index in range(k, len(values)):
        value = values[index]
        if value < -heap[0]:
            heapq.heapreplace(heap, -value)
    return sorted(-value for value in heap)
