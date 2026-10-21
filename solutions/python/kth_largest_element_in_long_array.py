import heapq

def find_kth_largest_unknown_length(stream, k):
    largest = []
    for value in stream:
        if len(largest) < k:
            heapq.heappush(largest, value)
        elif value > largest[0]:
            heapq.heapreplace(largest, value)
    return largest[0]
