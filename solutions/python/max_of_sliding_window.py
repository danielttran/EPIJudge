from collections import deque, namedtuple
TrafficElement = namedtuple('TrafficElement', 'time volume')

def calculate_traffic_volumes(traffic, width):
    candidates = deque()
    result = []
    for entry in traffic:
        while candidates and candidates[0].time < entry.time - width:
            candidates.popleft()
        while candidates and candidates[-1].volume <= entry.volume:
            candidates.pop()
        candidates.append(entry)
        result.append(TrafficElement(entry.time, candidates[0].volume))
    return result
