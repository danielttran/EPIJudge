def has_three_sum(values, target):
    ordered = sorted(values)
    for first in ordered:
        left, right = 0, len(ordered) - 1
        while left <= right:
            total = first + ordered[left] + ordered[right]
            if total == target:
                return True
            if total < target:
                left += 1
            else:
                right -= 1
    return False
