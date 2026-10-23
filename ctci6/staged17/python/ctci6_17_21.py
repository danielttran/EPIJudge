def HistogramWaterVolume(heights: list[int]) -> int:
    left, right = 0, len(heights) - 1
    left_max = right_max = volume = 0
    while left <= right:
        if left_max <= right_max:
            left_max = max(left_max, heights[left])
            volume += left_max - heights[left]
            left += 1
        else:
            right_max = max(right_max, heights[right])
            volume += right_max - heights[right]
            right -= 1
    return volume
