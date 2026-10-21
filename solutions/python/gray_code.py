def gray_code(num_bits):
    return [value ^ (value >> 1) for value in range(1 << num_bits)]


def differ_by_1_bit(first, second):
    changed = first ^ second
    return changed != 0 and (changed & (changed - 1)) == 0
