import math

def generate_first_k_a_b_sqrt2(k):
    if k <= 0:
        return []
    pairs = [(0, 0)]
    result = [0.0]
    one = root = 0
    square_root = math.sqrt(2)
    while len(result) < k:
        a, b = pairs[one]
        first = (a + 1, b)
        a, b = pairs[root]
        second = (a, b + 1)
        following = min((first, second), key=lambda p: p[0] + p[1] * square_root)
        pairs.append(following)
        result.append(following[0] + following[1] * square_root)
        one += first == following
        root += second == following
    return result
