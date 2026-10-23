def Urlify(buffer: list[str], trueLength: int) -> None:
    write = len(buffer) - 1
    for read in range(trueLength - 1, -1, -1):
        current = buffer[read]
        if current == " ":
            buffer[write] = "0"
            buffer[write - 1] = "2"
            buffer[write - 2] = "%"
            write -= 3
        else:
            buffer[write] = current
            write -= 1
