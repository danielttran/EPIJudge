def permutations(values):
    result = []
    def search(position):
        if position == len(values):
            result.append(values.copy())
            return
        for selected in range(position, len(values)):
            values[position], values[selected] = values[selected], values[position]
            search(position + 1)
            values[position], values[selected] = values[selected], values[position]
    search(0)
    return result
