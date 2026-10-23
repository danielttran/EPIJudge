def Compress(text: str) -> str:
    parts = []
    start = 0
    while start < len(text):
        end = start + 1
        while end < len(text) and text[end] == text[start]:
            end += 1
        parts.append(text[start])
        parts.append(str(end - start))
        start = end
    output = ''.join(parts)
    return output if len(output) < len(text) else text
