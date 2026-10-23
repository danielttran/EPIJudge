def SolveJigsaw(size: int, pieces: list[list[int]]) -> list[list[int]]:
    count = len(pieces)
    placed = [None] * count
    used = [False] * count

    def edge(index, turn, side):
        return pieces[index][(side - turn) % 4]

    def search(position):
        if position == count:
            return True
        row, column = divmod(position, size)
        for index in range(count):
            if used[index]:
                continue
            for turn in range(4):
                values = [edge(index, turn, s) for s in range(4)]
                if any(
                    (value == 0) != boundary
                    for value, boundary in zip(
                        values, (row == 0, column == size - 1, row == size - 1, column == 0)
                    )
                ):
                    continue
                if row and values[0] != -edge(*placed[position - size], 2):
                    continue
                if column and values[3] != -edge(*placed[position - 1], 1):
                    continue
                used[index] = True
                placed[position] = (index, turn)
                if search(position + 1):
                    return True
                used[index] = False
        return False

    return [list(pair) for pair in placed] if search(0) else []
