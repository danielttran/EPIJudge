import heapq

def find_closest_elements_in_sorted_arrays(sorted_arrays):
    heap = [(values[0], i, 0) for i, values in enumerate(sorted_arrays)]
    heapq.heapify(heap)
    maximum = max(value for value, _, _ in heap)
    best = maximum - heap[0][0]
    while True:
        minimum, index, position = heapq.heappop(heap)
        best = min(best, maximum - minimum)
        position += 1
        if position == len(sorted_arrays[index]):
            return best
        value = sorted_arrays[index][position]
        maximum = max(maximum, value)
        heapq.heappush(heap, (value, index, position))
