def LongestOnesAfterFlip(word: int) -> int:
    bits = word & 0xFFFFFFFF
    left = zeros = best = 0
    for right in range(32):
        if ((bits >> right) & 1) == 0:
            zeros += 1
        while zeros > 1:
            if ((bits >> left) & 1) == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
