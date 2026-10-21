import heapq

def sort_k_increasing_decreasing_array(values):
    runs = []
    start = 0
    while start < len(values):
        end = start + 1
        increasing = end == len(values) or values[end] >= values[start]
        while end < len(values) and (values[end] >= values[end - 1] if increasing else values[end] <= values[end - 1]):
            end += 1
        run = values[start:end]
        if not increasing:
            run.reverse()
        runs.append(run)
        start = end
    heap = [(run[0], i, 0) for i, run in enumerate(runs)]
    heapq.heapify(heap)
    result = []
    while heap:
        value, run, position = heapq.heappop(heap)
        result.append(value)
        position += 1
        if position < len(runs[run]):
            heapq.heappush(heap, (runs[run][position], run, position))
    return result
