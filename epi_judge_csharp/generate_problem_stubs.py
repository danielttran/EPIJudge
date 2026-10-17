#!/usr/bin/env python3
"""Create any missing C# judge stubs from the shared test-data catalog."""

import json
import re
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path(__file__).resolve().parent
CATALOG = PROJECT / "problem_catalog.json"
PROBLEMS = PROJECT / "Problems"
PROGRAM = PROJECT / "Program.cs"
MAPPING = ROOT / "problem_mapping.js"
UNORDERED_RESULT_PROBLEMS = {
    "combinations",
    "k_largest_in_heap",
    "phone_number_mnemonic",
    "valid_ip_addresses",
}


def split_types(value: str) -> List[str]:
    parts = []
    depth = 0
    start = 0
    for index, character in enumerate(value):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            parts.append(value[start:index].strip())
            start = index + 1
    parts.append(value[start:].strip())
    return parts


def inner_type(value: str, name: str) -> Optional[str]:
    prefix = name + "("
    if value.startswith(prefix) and value.endswith(")"):
        return value[len(prefix):-1]
    return None


def csharp_type(grammar: str, nullable_node: bool = True) -> str:
    primitive = {
        "bool": "bool",
        "float": "double",
        "int": "int",
        "long": "long",
        "string": "string",
    }
    if grammar in primitive:
        return primitive[grammar]
    inner = inner_type(grammar, "array")
    if inner is not None:
        return f"List<{csharp_type(inner)}>"
    inner = inner_type(grammar, "set")
    if inner is not None:
        return f"HashSet<{csharp_type(inner)}>"
    inner = inner_type(grammar, "binary_tree")
    if inner is not None:
        suffix = "?" if nullable_node else ""
        return f"BinaryTreeNode<{csharp_type(inner)}>{suffix}"
    inner = inner_type(grammar, "linked_list")
    if inner is not None:
        suffix = "?" if nullable_node else ""
        return f"ListNode<{csharp_type(inner)}>{suffix}"
    inner = inner_type(grammar, "tuple")
    if inner is not None:
        parts = split_types(inner)
        if not 2 <= len(parts) <= 4:
            raise ValueError(f"Unsupported tuple type: {grammar}")
        return f"({', '.join(csharp_type(part) for part in parts)})"
    if grammar == "void":
        return "void"
    raise ValueError(f"Unsupported type in catalog: {grammar}")


def class_name(problem_id: str) -> str:
    name = "".join(part[:1].upper() + part[1:] for part in problem_id.split("_"))
    if not name or not name[0].isalpha():
        name = "Problem" + name
    return name


def file_to_problem_id(language: str, filename: str) -> str:
    stem = Path(filename).stem
    if language in ("C++", "Python"):
        return stem
    if language == "Java":
        stem = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", stem)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", stem).lower()
    return ""


def test_case_count(problem_id: str) -> int:
    path = ROOT / "test_data" / f"{problem_id}.tsv"
    with path.open(encoding="utf-8") as test_data:
        return max(0, sum(1 for _ in test_data) - 1)


def update_dashboard_mapping(problems: List[dict]) -> int:
    raw = MAPPING.read_text(encoding="utf-8")
    prefix, contents = raw.split("=", 1)
    mapping = json.loads(contents.strip().rstrip(";"))

    # Rebuild C# entries from the catalog. Keep their recorded progress, but
    # remove the old entries first so repeated generation is idempotent.
    old_csharp_entries = {}
    for chapter, chapter_problems in list(mapping.items()):
        for title, languages in list(chapter_problems.items()):
            for language in list(languages):
                if language.startswith("C#: "):
                    old_csharp_entries[language] = languages.pop(language)
            if chapter == "C# Additional Problems" and not languages:
                del chapter_problems[title]

    locations = {}
    for chapter, chapter_problems in mapping.items():
        for title, languages in chapter_problems.items():
            for entry in languages:
                if not entry.startswith(("C++: ", "Java: ", "Python: ")):
                    continue
                language, filename = entry.split(": ", 1)
                problem_id = file_to_problem_id(language, filename)
                if problem_id:
                    locations.setdefault(problem_id, (chapter, title, languages))

    additional = mapping.setdefault("C# Additional Problems", {})
    occupied_rows = set()
    for problem in problems:
        problem_id = problem["id"]
        csharp_entry = f"C#: {class_name(problem_id)}.cs"
        if problem_id in locations:
            chapter, title, languages = locations[problem_id]
            row_identity = id(languages)
            if row_identity in occupied_rows:
                # The dashboard shows only one source per language in a row.
                # Keep similarly titled exercises separate so neither link is
                # hidden by the first C# entry.
                title = f"Additional: {problem_id.replace('_', ' ')}"
                languages = additional.setdefault(title, {})
                row_identity = id(languages)
        else:
            title = f"Additional: {problem_id.replace('_', ' ')}"
            languages = additional.setdefault(title, {})
            row_identity = id(languages)

        if row_identity in occupied_rows:
            raise ValueError(f"Could not create a unique dashboard row for {problem_id}.")
        occupied_rows.add(row_identity)
        progress = old_csharp_entries.get(csharp_entry, {}).get("passed", 0)
        languages[csharp_entry] = {
            "passed": progress,
            "total": test_case_count(problem_id),
        }

    rendered = prefix.rstrip() + " = " + json.dumps(mapping, indent=4) + ";\n"
    with MAPPING.open("w", encoding="utf-8", newline="\n") as output:
        output.write(rendered)
    return len(problems)


def type_of(grammar: str) -> str:
    return f"typeof({csharp_type(grammar, nullable_node=False)})"


def render_problem(problem: dict) -> str:
    problem_id = problem["id"]
    arguments = problem["argumentTypes"]
    result = problem["resultType"]
    parameters = [f"{csharp_type(argument)} arg{index + 1}" for index, argument in enumerate(arguments)]
    invocations = [f"({csharp_type(argument)})values[{index}]!" for index, argument in enumerate(arguments)]
    names = "new[] { " + ", ".join(f'"arg{index + 1}"' for index in range(len(arguments))) + " }"
    types = "new[] { " + ", ".join(type_of(argument) for argument in arguments) + " }"
    solve_call = "Solve(" + ", ".join(invocations) + ")"

    if result == "void":
        solve = "    public static void Solve(" + ", ".join(parameters) + ")\n    {\n        // TODO - implement this problem.\n        throw new NotImplementedException();\n    }"
        runner = (
            f"    public static int Run(string[] args) =>\n"
            f"        GenericTest.RunVoid(args, \"{problem['testDataFile']}\", {names}, {types},\n"
            f"            values => {solve_call});"
        )
    else:
        result_type = csharp_type(result)
        comparator = ""
        if problem_id in UNORDERED_RESULT_PROBLEMS:
            comparator = (
                f", (expected, actual) => GenericTest.UnorderedEquals(expected, actual, "
                f"{type_of(result)})"
            )
        solve = (
            f"    public static {result_type} Solve({', '.join(parameters)})\n"
            f"    {{\n        // TODO - implement this problem.\n"
            f"        return default!;\n    }}"
        )
        runner = (
            f"    public static int Run(string[] args) =>\n"
            f"        GenericTest.Run(args, \"{problem['testDataFile']}\", {names}, {types},\n"
            f"            {type_of(result)}, values => {solve_call}{comparator});"
        )

    return (
        "using EpiJudge.TestFramework;\n\n"
        "namespace EpiJudge.Problems;\n\n"
        f"public static class {class_name(problem_id)}\n"
        "{\n"
        f"{solve}\n\n"
        f"{runner}\n"
        "}\n"
    )


def render_program(problems: List[dict]) -> str:
    cases = "\n".join(
        f'    "{problem["id"]}" => {class_name(problem["id"])}.Run(judgeArgs),'
        for problem in problems
    )
    return (
        "using EpiJudge.Problems;\n\n"
        "if (args.Length == 0)\n"
        "{\n"
        "    Console.Error.WriteLine(\"Usage: dotnet run --project epi_judge_csharp -- <problem> [judge options]\");\n"
        "    Console.Error.WriteLine(\"See epi_judge_csharp/problem_catalog.json for problem IDs.\");\n"
        "    return 2;\n"
        "}\n\n"
        "var judgeArgs = args[1..];\n"
        "return args[0] switch\n"
        "{\n"
        f"{cases}\n"
        "    _ => UnknownProblem(args[0]),\n"
        "};\n\n"
        "static int UnknownProblem(string problem)\n"
        "{\n"
        "    Console.Error.WriteLine($\"Unknown problem: {problem}\");\n"
        "    return 2;\n"
        "}\n"
    )


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["problems"]
    class_names = [class_name(problem["id"]) for problem in catalog]
    if len(class_names) != len(set(class_names)):
        raise ValueError("Problem IDs produce duplicate C# class names.")

    PROBLEMS.mkdir(exist_ok=True)
    created = 0
    for problem in catalog:
        path = PROBLEMS / f"{class_name(problem['id'])}.cs"
        if path.exists():
            continue
        with path.open("w", encoding="utf-8", newline="\n") as source:
            source.write(render_problem(problem))
        created += 1

    with PROGRAM.open("w", encoding="utf-8", newline="\n") as source:
        source.write(render_program(catalog))
    mapped = update_dashboard_mapping(catalog)
    print(f"Created {created} C# stubs, registered {len(catalog)} problems, and added {mapped} dashboard entries.")


if __name__ == "__main__":
    main()
