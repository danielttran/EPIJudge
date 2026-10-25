# Problem patterns and hints

The existing bank is unchanged. `problemGuidance.json` provides one reviewed
primary technique tag and two opt-in hints for every runnable problem ID.
The first hint is a technique-level observation prompt unless an explicit
problem-specific observation is supplied in `overrides.json`. The second starts
from the existing independently authored strategy, with reviewed overrides where
language-specific return types, mutation contracts or important variant rules
make that paragraph unsuitable as a shared hint. These are learning aids, not new solutions or
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

## Follow-up content and UI audit

Reviewed all 465 problem statements against their primary tags and second hints,
and checked the shared first prompts for applicability. Corrected the sorting-window
tag to Linear scan (the input is not transformed) and black-border square to Dynamic
programming (directional run lengths, not array mutation). Explicit overrides refine
64 first hints and 22 strategy hints, including node-versus-value returns, native
in-place buffers, required negative stock profits, and endpoint/bit-width rules.
The other first prompts remain technique-level prompts, not individually authored
observations. No solution code or judge contract was changed.

Regression tests cover variant distinctions and cross-language output guidance.
UI checks include focus after reveal/hide, accessible pattern descriptions, all
pattern filters and every library row at three widths in both themes, browser
Back/Forward resets, and zoomed hint controls. Labels have a 12px minimum instead
of inheriting the legacy row's 10px secondary-text rule. Browser checks verify
rendering and interaction, not semantic correctness of prose; the content review
and contract-specific tests are separate evidence.

## Additional three-pass audit

1. Numeric contracts: removed remaining language-specific numeric-type advice from
   nine shared strategy hints. In particular, the floor-coverage recurrence asks for
   an exact representable result; saturating at a C# integer limit is not a universal
   contract. Clarified exact intermediates and 64-bit representation handling.
2. Interaction/layout: reproduced a real 568x320 landscape failure where fixed
   library controls squeezed the list below one row. The short-window drawer now
   scrolls as a whole while retaining at least two rows of list height. Added empty
   search, Escape/reopen and final-row-selection checks and a landscape screenshot.
3. Regression: added repeated reveal/hide focus cycles and numeric-hint tests,
   rechecked exact 465-ID guidance coverage, every pattern filter, all five language
   solution records, and the production build. No solution or judge code was edited.
