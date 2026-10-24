# Problem patterns and hints

The existing bank is unchanged. `problemGuidance.json` provides one reviewed
primary technique tag and two opt-in hints for every runnable problem ID.
The first hint is a technique-level observation prompt; the second is the
problem-specific strategy from the existing independently authored C# explanation,
with C#-specific tail notes removed. These are learning aids, not new solutions or
claims that every valid solution must use the tagged technique. Examples such as
sorted EPI Two Sum and unsorted Blind 75 Two Sum deliberately have different tags.

Hints appear at the bottom of **Problem**, never in **Solution**. They start
hidden, reveal sequentially, can be collapsed/hidden, and reset on navigation to
another problem. Switching solution languages does not affect editor drafts.
The library supports exact pattern filters and tag text in its existing search.
No new course, session, grading or persistence behavior is introduced.

Assignments in `build_catalog.py` are explicit, not inferred from titles or
keywords. Review against the problem contract and supported solution before
changing a tag. Add new catalog IDs deliberately: missing/extra/duplicate IDs
fail generation. Update the output after relevant explanation changes:

```
python scripts/guidance/build_catalog.py
python scripts/guidance/build_catalog.py --check
npm --prefix epijudge.client run test:coverage
npm --prefix epijudge.client run build
```

The guidance workflow builds the real app, uses isolated practice storage and
Chromium, compares rendered tags/hints for the entire live bank, checks narrow,
medium and desktop views in both themes, tests keyboard expansion, verifies the
Solution view excludes hints, checks draft preservation across five solution
languages, and exercises pattern filtering/search. Screenshots and a JSON report
are uploaded as `guidance-browser-audit`. Rendered checks are not algorithm tests;
existing execution workflows continue to validate those separately.
