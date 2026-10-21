"""Typed C++ calls and contract checks for the original Interview Cake bank harness."""


def configuration(spec):
    mode = spec["mode"]
    method = spec["method"]
    class_name = spec["className"]
    body = []
    if mode in ("queue", "stack", "trie", "temperature"):
        body += [
            f"{class_name} instance;",
            "json output = json::array();",
            "int count = 0;",
            "for (size_t i = 0; i < raw[0].size(); ++i) {",
            "    std::string op = raw[0][i].get<std::string>();",
            "    const auto& values = raw[1][i];",
        ]
        empty = (
            (
                'op == "Dequeue"'
                if mode == "queue"
                else '(op == "Pop" || op == "GetMax")'
            )
            if mode in ("queue", "stack")
            else "false"
        )
        body += [
            f"    bool empty = count == 0 && ({empty});",
            "    json result = nullptr;",
            "    try {",
        ]
        operations = {
            "queue": [
                ("Enqueue", "instance.Enqueue(values[0].get<int>());", False),
                ("Dequeue", "result = dump(instance.Dequeue());", True),
            ],
            "stack": [
                ("Push", "instance.Push(values[0].get<int>());", False),
                ("Pop", "result = dump(instance.Pop());", True),
                ("GetMax", "result = dump(instance.GetMax());", True),
            ],
            "trie": [
                (
                    "AddWord",
                    "result = dump(instance.AddWord(values[0].get<std::string>()));",
                    True,
                )
            ],
            "temperature": [("Insert", "instance.Insert(values[0].get<int>());", False)]
            + [
                (op, f"result = dump(instance.{op}());", True)
                for op in ("GetMin", "GetMax", "GetMean", "GetMode")
            ],
        }[mode]
        for i, (op, call, _) in enumerate(operations):
            body.append(
                f'        {"if" if i == 0 else "else if"} (op == "{op}") {{ {call} }}'
            )
        body += [
            '        else throw ContractError("Unknown state operation.");',
            '        check(!empty, "Empty-state operation must signal an error.");',
            "    } catch (const ContractError&) { throw; }",
            '      catch (const std::exception&) { if (!empty) throw; result = {{"error", "empty"}}; }',
            "    output.push_back(result);",
            '    if (op == "Enqueue" || op == "Push") ++count;',
            '    else if ((op == "Dequeue" || op == "Pop") && !empty) --count;',
            "}",
            "return output;",
        ]
    elif mode == "wordcloud":
        body = [
            f"{class_name} instance(raw[0].get<std::string>());",
            "return dump(instance.WordsToCounts);",
        ]
    elif mode in ("shuffle", "rand5", "rand7"):
        if mode == "shuffle":
            body = [
                f"return randomCheck<{class_name}>(raw, true, 0, 0, []({class_name}& instance, std::vector<int>& array) -> json {{ instance.{method}(array); return nullptr; }});"
            ]
        else:
            maximum, outcomes = (7, 5) if mode == "rand5" else (5, 7)
            body = [
                f"return randomCheck<{class_name}>(raw, false, {maximum}, {outcomes}, []({class_name}& instance, std::vector<int>&) -> json {{ return instance.{method}(); }});"
            ]
    elif mode == "cycle":
        body = [
            "auto head = readList(raw[0]);",
            "auto nodes = listNodes(head);",
            "int index = raw[1].get<int>();",
            "if (index >= 0) nodes.back()->Next = nodes.at(index);",
            "std::vector<std::pair<int, LinkedListNode*>> before;",
            "for (auto node : nodes) before.push_back({node->Value, node->Next});",
            f"{class_name} instance; auto actual = instance.{method}(head);",
            "for (size_t i = 0; i < nodes.size(); ++i)",
            '    check(std::make_pair(nodes[i]->Value, nodes[i]->Next) == before[i], "Cycle detection modified the list.");',
            "return dump(actual);",
        ]
    elif mode == "delete":
        body = [
            "auto head = readList(raw[0]);",
            "auto nodes = listNodes(head);",
            "int index = raw[1].get<int>();",
            "std::vector<std::pair<int, LinkedListNode*>> before;",
            "for (auto node : nodes) before.push_back({node->Value, node->Next});",
            f"{class_name} instance; instance.{method}(nodes.at(index));",
            "for (size_t i = 0; i < nodes.size(); ++i)",
            '    check(std::make_pair(nodes[i]->Value, nodes[i]->Next) == before[i == static_cast<size_t>(index) ? i + 1 : i], "Deletion violated target/successor alias semantics.");',
            "return dump(head);",
        ]
    elif mode == "reverse_list":
        body = [
            "auto head = readList(raw[0]);",
            "auto nodes = listNodes(head);",
            "std::vector<int> values; for (auto node : nodes) values.push_back(node->Value);",
            f"{class_name} instance; auto result = instance.{method}(head);",
            "auto after = listNodes(result); auto expected = nodes; std::reverse(expected.begin(), expected.end());",
            'check(after == expected, "Reversal must reuse the original nodes in reverse order.");',
            'for (size_t i = 0; i < nodes.size(); ++i) check(nodes[i]->Value == values[i], "Reversal changed node values.");',
            "return dump(result);",
        ]
    else:
        decoders = {
            "tree": "readTree({raw})",
            "list": "readList({raw})",
            "graph": "readGraph({raw})",
            "meetings": "readMeetings({raw})",
            "rect": "readRect({raw})",
            "cakes": "readCakes({raw})",
            "chars": "readChars({raw})",
            "i": "{raw}.get<int>()",
            "l": "{raw}.get<long long>()",
            "s": "{raw}.get<std::string>()",
            "files": "{raw}.get<std::string>()",
            "ai": "{raw}.get<std::vector<int>>()",
            "as": "{raw}.get<std::vector<std::string>>()",
            "map": "{raw}.get<std::unordered_map<std::string, std::vector<std::string>>>()",
        }
        for i, param in enumerate(spec["params"]):
            body.append(
                f"auto a{i} = " + decoders[param["type"]].format(raw=f"raw[{i}]") + ";"
            )
        args = ", ".join("a" + str(i) for i in range(len(spec["params"])))
        body.append(f"{class_name} instance;")
        if mode in ("chars", "words"):
            body += [
                "auto originalSize = a0.size();",
                f"instance.{method}({args});",
                'check(a0.size() == originalSize, "Character array length changed.");',
                "return dump(a0);",
            ]
        elif mode == "color":
            body += [
                "auto originalNodes = a0; auto originalPalette = a1;",
                "std::vector<std::unordered_set<GraphNode*>> originalEdges;",
                "std::vector<std::string> originalLabels;",
                "for (auto node : a0) { originalEdges.push_back(node->Neighbors); originalLabels.push_back(node->Label); }",
                f"instance.{method}({args});",
                'check(a0 == originalNodes && a1 == originalPalette, "Graph nodes or palette were modified.");',
                "for (size_t i = 0; i < originalNodes.size(); ++i) {",
                "    auto node = originalNodes[i];",
                '    check(node->Label == originalLabels[i] && node->Neighbors == originalEdges[i], "Graph labels or edges were modified.");',
                '    check(std::find(originalPalette.begin(), originalPalette.end(), node->Color) != originalPalette.end(), "Color is outside the palette.");',
                '    for (auto neighbor : node->Neighbors) check(neighbor->Color != node->Color, "Adjacent vertices share a color.");',
                "}",
                "return true;",
            ]
        else:
            for i, _ in enumerate(spec["params"]):
                body.append(f"auto preserve{i} = preserve(a{i});")
            if mode == "files":
                body.append("auto beforeFiles = filesSnapshot(a0);")
            checks = " ".join(f"preserve{i}();" for i, _ in enumerate(spec["params"]))
            # The infinity result is a semantic sentinel, with preservation checked on that branch too.
            body += [
                "try {",
                f"    auto actual = instance.{method}({args});",
                "    " + checks,
            ]
            if mode == "files":
                body += [
                    '    check(filesSnapshot(a0) == beforeFiles, "Filesystem must remain unchanged.");'
                ]
            if mode == "kth":
                body += [
                    "    auto nodes = listNodes(a1); auto found = std::find(nodes.begin(), nodes.end(), actual);",
                    '    check(found != nodes.end(), "Return an original node reference.");',
                    "    return static_cast<int>(found - nodes.begin());",
                ]
            elif mode == "meetings":
                body += [
                    "    for (auto meeting : actual)",
                    '        check(meeting && std::find(a0.begin(), a0.end(), meeting) == a0.end(), "Return new meeting objects.");',
                    "    return dump(actual);",
                ]
            elif mode == "rect":
                body += [
                    '    check(actual && actual != a0 && actual != a1, "Return a new rectangle.");',
                    "    return dump(actual);",
                ]
            elif mode == "path":
                body += [
                    "    if (actual.empty()) return nullptr;",
                    "    return dump(actual);",
                ]
            else:
                body.append("    return dump(actual);")
            body += [
                "} catch (const InfinityException&) {",
                "    " + checks,
                '    return {{"error", "infinite"}};',
                "}",
            ]
    return (
        "json execute(const json& raw) {\n"
        + "\n".join("    " + line for line in body)
        + "\n}\n"
    )
