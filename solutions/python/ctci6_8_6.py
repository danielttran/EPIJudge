def SolveHanoi(disks: int) -> list[list[int]]:
    towers = [list(range(disks, 0, -1)), [], []]
    moves = []

    def transfer(count, source, buffer, destination):
        if count == 0:
            return
        transfer(count - 1, source, destination, buffer)
        disk = towers[source].pop()
        towers[destination].append(disk)
        moves.append([disk, source, destination])
        transfer(count - 1, buffer, source, destination)

    transfer(disks, 0, 1, 2)
    return moves
