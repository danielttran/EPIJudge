"""Report book/judge coverage without conflating exercise identities and TSV files."""
import ast
from collections import defaultdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit():
    corpus = {path.name for path in (ROOT / 'test_data').glob('*.tsv')}
    entrypoints = defaultdict(list)
    for path in sorted((ROOT / 'epi_judge_python').glob('*.py')):
        for call in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                    and call.func.attr == 'generic_test_main' and len(call.args) > 1
                    and isinstance(call.args[1], ast.Constant)):
                entrypoints[call.args[1].value].append(path.stem)
    mapping = json.loads((ROOT / 'scripts/problem-mapping.json').read_text(encoding='utf-8'))
    guide = json.loads((ROOT / 'epijudge.client/src/studyGuide.json').read_text(encoding='utf-8'))
    companions = json.loads((ROOT / 'epijudge.client/src/reading/content/lessons.json').read_text(encoding='utf-8'))
    by_reference = {reference: lesson['id'] for lesson in companions for reference in lesson['bookReferences']}
    plans = []
    seen = set()
    for column, entries in enumerate(guide['columns']):
        for entry in entries:
            if entry['number'] in seen:
                continue
            seen.add(entry['number'])
            if entry['problemId'] is None:
                plans.append({'number': entry['number'], 'title': entry['title'], 'column': column, 'reason': entry['reason'],
                              'readingCompanionId': by_reference.get(entry['number'])})
    return {
        'testCorpora': len(corpus),
        'pythonJudgeEntrypoints': sum(map(len, entrypoints.values())),
        'historicalIndexHeadings': sum(map(len, mapping.values())),
        'sharedCorpora': {name: names for name, names in entrypoints.items() if len(names) > 1},
        'missingCorpora': sorted(set(entrypoints) - corpus),
        'corporaWithoutPythonEntrypoint': sorted(corpus - set(entrypoints)),
        'unavailableGuideReferences': plans,
        'originalReadingCompanions': len(companions),
        'guideReferencesWithoutCompanionsOrGraders': [entry['number'] for entry in plans if not entry['readingCompanionId']],
        'guideSource': guide['tableSource'],
        'guideVerification': guide['verification'],
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
