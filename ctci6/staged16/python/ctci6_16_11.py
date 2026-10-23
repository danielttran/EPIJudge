def DivingBoardLengths(planks: int, shorter: int, longer: int) -> list[int]:
    if shorter == longer:
        return [planks * shorter]
    return [planks * shorter + count * (longer - shorter) for count in range(planks + 1)]
