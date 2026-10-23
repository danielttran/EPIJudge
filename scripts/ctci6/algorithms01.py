"""Original chapter-one algorithms; bindings expand only bank-owned templates.

Native languages share the same algorithm where its proof is shared. Binding
differences are explicit, and all emitted languages must be executed separately.
"""

from textwrap import dedent


def native(ref, language):
    def length(value):
        return (
            value + ".Length"
            if language == "csharp"
            else value + ".length"
            if language == "java" and value in ("buffer", "matrix", "matrix[0]")
            else value + ".length()"
            if language == "java"
            else "static_cast<int>(" + value + ".size())"
        )

    def at(value, index):
        return (
            value + ".charAt(" + index + ")"
            if language == "java"
            else value + "[" + index + "]"
        )

    def flags(name, size):
        return {
            "csharp": f"bool[] {name} = new bool[{size}];",
            "java": f"boolean[] {name} = new boolean[{size}];",
            "cpp": f"std::vector<bool> {name}({size}, false);",
        }[language]

    counts = {
        "csharp": "int[] counts = new int[128];",
        "java": "int[] counts = new int[128];",
        "cpp": "std::array<int,128> counts{};",
    }[language]
    n, m = length("first"), length("second")
    if ref == "1.1":
        return f"""{flags("seen", 128)}
for (int i = 0; i < {length("text")}; ++i) {{
    int code = {at("text", "i")};
    if (seen[code]) return false;
    seen[code] = true;
}}
return true;"""
    if ref == "1.2":
        return f"""if ({n} != {m}) return false;
{counts}
for (int i = 0; i < {n}; ++i) ++counts[{at("first", "i")}];
for (int i = 0; i < {m}; ++i) {{
    int code = {at("second", "i")};
    --counts[code];
    if (counts[code] < 0) return false;
}}
return true;"""
    if ref == "1.3":
        return f"""int write = {length("buffer")} - 1;
for (int read = trueLength - 1; read >= 0; --read) {{
    char current = buffer[read];
    if (current == ' ') {{
        buffer[write--] = '0';
        buffer[write--] = '2';
        buffer[write--] = '%';
    }} else {{
        buffer[write--] = current;
    }}
}}"""
    if ref == "1.4":
        return f"""{counts}
for (int i = 0; i < {length("text")}; ++i) {{
    int code = {at("text", "i")};
    if (code >= 65 && code <= 90) code += 32;
    if (code >= 97 && code <= 122) ++counts[code];
}}
int odd = 0;
for (int code = 97; code <= 122; ++code) odd += counts[code] % 2;
return odd <= 1;"""
    if ref == "1.5":
        return f"""int n = {n}, m = {m};
if (n - m > 1 || m - n > 1) return false;
int i = 0, j = 0;
bool used = false;
while (i < n && j < m) {{
    if ({at("first", "i")} == {at("second", "j")}) {{ ++i; ++j; }}
    else {{
        if (used) return false;
        used = true;
        if (n >= m) ++i;
        if (m >= n) ++j;
    }}
}}
return true;""".replace(
            "bool used", "boolean used" if language == "java" else "bool used"
        )
    if ref == "1.6":
        builder = {
            "csharp": "var output = new System.Text.StringBuilder();",
            "java": "StringBuilder output = new StringBuilder();",
            "cpp": "std::string output;",
        }[language]
        append = {
            "csharp": f"output.Append({at('text', 'start')}); output.Append(end - start);",
            "java": f"output.append({at('text', 'start')}); output.append(end - start);",
            "cpp": "output.push_back(text[start]); output += std::to_string(end - start);",
        }[language]
        result = {
            "csharp": "output.ToString()",
            "java": "output.toString()",
            "cpp": "output",
        }[language]
        outlength = {
            "csharp": "output.Length",
            "java": "output.length()",
            "cpp": "static_cast<int>(output.size())",
        }[language]
        return f"""{builder}
int n = {length("text")};
for (int start = 0; start < n;) {{
    int end = start + 1;
    while (end < n && {at("text", "end")} == {at("text", "start")}) ++end;
    {append}
    start = end;
}}
return {outlength} < n ? {result} : text;"""
    if ref == "1.7":
        return f"""int n = {length("matrix")};
for (int r = 0; r < n; ++r) {{
    for (int c = r + 1; c < n; ++c) {{
        int saved = matrix[r][c]; matrix[r][c] = matrix[c][r]; matrix[c][r] = saved;
    }}
}}
for (int r = 0; r < n; ++r) {{
    for (int c = 0; c < n / 2; ++c) {{
        int saved = matrix[r][c]; matrix[r][c] = matrix[r][n - 1 - c]; matrix[r][n - 1 - c] = saved;
    }}
}}"""
    if ref == "1.8":
        return f"""int rows = {length("matrix")};
if (rows == 0) return;
int cols = {length("matrix[0]")};
{flags("zeroRows", "rows")}
{flags("zeroCols", "cols")}
for (int r = 0; r < rows; ++r) {{
    for (int c = 0; c < cols; ++c) {{
        if (matrix[r][c] == 0) {{ zeroRows[r] = true; zeroCols[c] = true; }}
    }}
}}
for (int r = 0; r < rows; ++r) {{
    for (int c = 0; c < cols; ++c) {{
        if (zeroRows[r] || zeroCols[c]) matrix[r][c] = 0;
    }}
}}"""
    if ref == "1.9":
        search = {
            "csharp": "(first + first).Contains(second, StringComparison.Ordinal)",
            "java": "(first + first).contains(second)",
            "cpp": "(first + first).find(second) != std::string::npos",
        }[language]
        return f"if ({n} == 0 || {n} != {m}) return false;\nreturn {search};"
    raise ValueError(ref)


PYTHON = {
    "1.1": """
seen = [False] * 128
for character in text:
    code = ord(character)
    if seen[code]:
        return False
    seen[code] = True
return True
""",
    "1.2": """
if len(first) != len(second):
    return False
counts = [0] * 128
for character in first:
    counts[ord(character)] += 1
for character in second:
    code = ord(character)
    counts[code] -= 1
    if counts[code] < 0:
        return False
return True
""",
    "1.3": """
write = len(buffer) - 1
for read in range(trueLength - 1, -1, -1):
    current = buffer[read]
    if current == ' ':
        buffer[write] = '0'
        buffer[write - 1] = '2'
        buffer[write - 2] = '%'
        write -= 3
    else:
        buffer[write] = current
        write -= 1
""",
    "1.4": """
counts = [0] * 128
for character in text:
    code = ord(character)
    if 65 <= code <= 90:
        code += 32
    if 97 <= code <= 122:
        counts[code] += 1
return sum(counts[code] % 2 for code in range(97, 123)) <= 1
""",
    "1.5": """
n, m = len(first), len(second)
if abs(n - m) > 1:
    return False
i = j = 0
used = False
while i < n and j < m:
    if first[i] == second[j]:
        i += 1
        j += 1
    else:
        if used:
            return False
        used = True
        if n >= m:
            i += 1
        if m >= n:
            j += 1
return True
""",
    "1.6": """
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
""",
    "1.7": """
n = len(matrix)
for r in range(n):
    for c in range(r + 1, n):
        matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
for r in range(n):
    for c in range(n // 2):
        matrix[r][c], matrix[r][n - 1 - c] = matrix[r][n - 1 - c], matrix[r][c]
""",
    "1.8": """
rows = len(matrix)
if rows == 0:
    return
cols = len(matrix[0])
zero_rows, zero_cols = [False] * rows, [False] * cols
for r in range(rows):
    for c in range(cols):
        if matrix[r][c] == 0:
            zero_rows[r] = True
            zero_cols[c] = True
for r in range(rows):
    for c in range(cols):
        if zero_rows[r] or zero_cols[c]:
            matrix[r][c] = 0
""",
    "1.9": """
if not first or len(first) != len(second):
    return False
return second in first + first
""",
}

JAVASCRIPT = {
    "1.1": """
const seen = Array(128).fill(false);
for (let i = 0; i < text.length; ++i) {
    const code = text.charCodeAt(i);
    if (seen[code]) return false;
    seen[code] = true;
}
return true;
""",
    "1.2": """
if (first.length !== second.length) return false;
const counts = Array(128).fill(0);
for (let i = 0; i < first.length; ++i) ++counts[first.charCodeAt(i)];
for (let i = 0; i < second.length; ++i) {
    const code = second.charCodeAt(i);
    if (--counts[code] < 0) return false;
}
return true;
""",
    "1.3": """
let write = buffer.length - 1;
for (let read = trueLength - 1; read >= 0; --read) {
    const current = buffer[read];
    if (current === ' ') {
        buffer[write--] = '0';
        buffer[write--] = '2';
        buffer[write--] = '%';
    } else {
        buffer[write--] = current;
    }
}
""",
    "1.4": """
const counts = Array(128).fill(0);
for (let i = 0; i < text.length; ++i) {
    let code = text.charCodeAt(i);
    if (code >= 65 && code <= 90) code += 32;
    if (code >= 97 && code <= 122) ++counts[code];
}
let odd = 0;
for (let code = 97; code <= 122; ++code) odd += counts[code] % 2;
return odd <= 1;
""",
    "1.5": """
const n = first.length, m = second.length;
if (Math.abs(n - m) > 1) return false;
let i = 0, j = 0, used = false;
while (i < n && j < m) {
    if (first[i] === second[j]) { ++i; ++j; }
    else {
        if (used) return false;
        used = true;
        if (n >= m) ++i;
        if (m >= n) ++j;
    }
}
return true;
""",
    "1.6": """
const parts = [];
for (let start = 0; start < text.length;) {
    let end = start + 1;
    while (end < text.length && text[end] === text[start]) ++end;
    parts.push(text[start], String(end - start));
    start = end;
}
const output = parts.join('');
return output.length < text.length ? output : text;
""",
    "1.7": """
const n = matrix.length;
for (let r = 0; r < n; ++r) {
    for (let c = r + 1; c < n; ++c) {
        const saved = matrix[r][c]; matrix[r][c] = matrix[c][r]; matrix[c][r] = saved;
    }
}
for (let r = 0; r < n; ++r) {
    for (let c = 0; c < Math.floor(n / 2); ++c) {
        const saved = matrix[r][c]; matrix[r][c] = matrix[r][n - 1 - c]; matrix[r][n - 1 - c] = saved;
    }
}
""",
    "1.8": """
const rows = matrix.length;
if (rows === 0) return;
const cols = matrix[0].length;
const zeroRows = Array(rows).fill(false), zeroCols = Array(cols).fill(false);
for (let r = 0; r < rows; ++r) {
    for (let c = 0; c < cols; ++c) {
        if (matrix[r][c] === 0) { zeroRows[r] = true; zeroCols[c] = true; }
    }
}
for (let r = 0; r < rows; ++r) {
    for (let c = 0; c < cols; ++c) {
        if (zeroRows[r] || zeroCols[c]) matrix[r][c] = 0;
    }
}
""",
    "1.9": """
if (first.length === 0 || first.length !== second.length) return false;
return (first + first).includes(second);
""",
}


def body(ref, language):
    if language == "python":
        return dedent(PYTHON[ref]).strip()
    if language == "javascript":
        return dedent(JAVASCRIPT[ref]).strip()
    return native(ref, language)
