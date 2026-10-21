def shortest_equivalent_path(path):
    absolute = path.startswith('/')
    components = []
    for part in path.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if components and components[-1] != '..':
                components.pop()
            elif not absolute:
                components.append(part)
        else:
            components.append(part)
    return ('/' if absolute else '') + '/'.join(components)
