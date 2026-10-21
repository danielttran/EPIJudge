def divide(dividend, divisor):
    if divisor <= 0:
        raise ValueError('The divisor must be positive')
    result = 0
    shift = max(0, dividend.bit_length() - divisor.bit_length())
    for bit in range(shift, -1, -1):
        candidate = divisor << bit
        if candidate <= dividend:
            dividend -= candidate
            result |= 1 << bit
    return result
