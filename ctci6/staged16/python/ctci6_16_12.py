def EncodeXml(
    elementNames: list[str],
    elementTexts: list[str],
    children: list[list[int]],
    attributeOwners: list[int],
    attributeNames: list[str],
    attributeValues: list[str],
    codeNames: list[str],
    codes: list[int],
) -> list[str]:
    if not elementNames:
        return []
    lookup = {name: str(code) for name, code in zip(codeNames, codes)}
    attributes = [[] for _ in elementNames]
    for index, owner in enumerate(attributeOwners):
        attributes[owner].append(index)
    result = []
    events = [(0, False)]
    while events:
        node, exiting = events.pop()
        if exiting:
            result.append("0")
            continue
        result.append(lookup[elementNames[node]])
        for attribute in attributes[node]:
            result.extend([lookup[attributeNames[attribute]], attributeValues[attribute]])
        result.append("0")
        events.append((node, True))
        if elementTexts[node]:
            result.append(elementTexts[node])
        else:
            for child in reversed(children[node]):
                events.append((child, False))
    return result
