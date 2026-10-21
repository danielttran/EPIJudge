"""Sanitized factual inventory, normalized from all seven verified transfer batches."""

import hashlib
import json

from specs import ROOT, S

facts = [
    (
        "No tree mutation. Valid BST; second-largest returns the integer key, not a node reference. Null/singleton reference rejects with ArgumentException. O(h) time, O(1) auxiliary.",
        "Duplicate policy/second-distinct interpretation unspecified; malformed/cyclic structures unspecified.",
    ),
    (
        "Exactly one earlier purchase and later sale at distinct indices. Declining prices require the least-negative feasible difference; equal prices yield zero. Read-only reference. Fewer than two prices: reference ArgumentException. O(n)/O(1).",
        "Null and numeric overflow unspecified.",
    ),
    (
        "Global maximum leaf depth minus minimum leaf depth <= 1; leaf has neither child. One-leaf chains pass. Empty reference true. Preserve tree. O(n) time, O(h) traversal storage, O(n) worst case.",
        "Cycles/shared-node non-trees unspecified.",
    ),
    (
        "Inherited ancestor restrictions, not just parent comparisons. Main references strict ordering and reject duplicates. No mutation. Recursive empty true; iterative lacks guard. Reference endpoint-bound bug is identified as a bonus issue, not a required rejection. O(n)/O(h).",
        "Empty behavior differs by reference. Full int range unresolved by base reference. Duplicate-placement variants are optional bonus.",
    ),
    (
        "Raw ASCII (), [], {} matching and nesting. Reject unmatched closer, wrong/crossing type, leftover opener. Reference ignores other characters, accepts empty/no-delimiter strings, scans delimiter characters inside quotes/comments. O(n)/O(n).",
        "Null unspecified.",
    ),
    (
        "Exact interleaving preserving each source order. IDs globally unique, not numerically sorted. Arrays read-only. Empty sources permitted, all-empty true. Extra/unknown/duplicated/missing served entries false. O(n)/O(1).",
        "Null unspecified. Duplicate source IDs outside domain.",
    ),
    (
        "F(0)=0, F(1)=1; recurrence is sum of prior two. Negative reference rejected (ArgumentException or ArgumentOutOfRangeException depending variant). O(n)/O(1); logarithmic bonus optional.",
        "Upper bound/overflow unspecified; exact negative-input exception subtype inconsistent.",
    ),
    (
        "Only target reference supplied, no head/predecessor. Required mutation logically removes target position by preserving target object but copying successor value/Next and bypassing successor. Aliases observe these effects. Non-tail normal domain; head allowed. Tail reference InvalidOperationException. O(1)/O(1).",
        "Null/cyclic input unspecified. Physical removal of target object is not reference behavior.",
    ),
    (
        "Cycle depends on node identity, not values; only reachable nodes matter. Preserve links/values. Empty false, single-null-next false, self-loop true, prefixed cycle true. O(n)/O(1).",
        "No unresolved valid-domain facts.",
    ),
    (
        "Read-only recursive filesystem search; full-path OriginalPath/DuplicatePath pairs denote suspected duplicates for human confirmation. At most one duplicate per original. Bounded sampling O(f) allows false positives; exact verification optional with byte-proportional cost. Later LastWriteTime reference labeled duplicate; heuristic fallible. Empty [] and nested/sibling search. Equal timestamps/traversal ties unspecified. O(f) fingerprints/paths.",
        "Controlled filesystem adapter needed. Missing/inaccessible paths, I/O failures, symlinks/hardlinks/directory cycles/concurrent changes unspecified. Output order, timestamp ties, proof of original, exact-vs-probabilistic judging unresolved.",
    ),
    (
        "Length n+1, entries 1..n. Any actual repeated value accepted, multiple repeated values and frequency >2 permitted. Non-destructive required. O(n log n)/O(1) target.",
        "Null/too-short/out-of-range outside valid domain; no rejection rule.",
    ),
    (
        "Same length/range domain as preceding task. Any repeated value, multiple duplicates/higher frequencies valid. Non-destructive required. O(n)/O(1) target.",
        "Null and invalid domain unspecified; no particular reference-selected duplicate required.",
    ),
    (
        "Rotated alphabetically ordered lowercase words, ordinal reference comparison; principal scenario actual internal wrap. Return zero-based wrap index. Read-only. Singleton reference 0. O(log n) comparisons, O(L log n) character work/O(1).",
        "Empty/null unspecified. Unrotated old reference last-index result is incidental, not mandatory. Duplicates/ambiguous wrap, null entries/non-lowercase collation unspecified.",
    ),
    (
        "Undirected node-reference graph with string Label, neighbor-reference set, writable Color. Mutate Color only; preserve graph identity/connectivity. Any valid assignment using maximum-degree-plus-one colors, enough distinct palette names. Color disconnected/isolated vertices. Empty returns. Self-edge reference ArgumentException. O(V+E) stated target; O(D) auxiliary.",
        "Initial colors, duplicate/insufficient palettes, nulls, omitted neighbors/asymmetric adjacency unspecified. Failure may partially recolor; no atomicity, color choice or order requirement.",
    ),
    (
        "Choose exactly three distinct positions, >=3 values. Signed ordering, negatives/zero/repeated values valid. Read-only reference. Short reference ArgumentException. O(n)/O(1).",
        "Null/overflow/input numeric limits unspecified.",
    ),
    (
        "QueueTwoStacks Enqueue/Dequeue state, retain each occurrence, FIFO any interleaving. Explicit two stacks, push/pop O(1). Empty new/drained reference InvalidOperationException. Total O(m), amortized O(1), storage queued count.",
        "Concurrency/capacity unspecified; no worst-case O(1) each Dequeue requirement.",
    ),
    (
        "In-place mutable array; preserve identity/length/multiset, duplicate values are distinct occurrences. Supplied inclusive GetRandom(lower,upper), unbiased full permutations intended. Empty/single no change. O(n) one pass/O(1).",
        "No seed/stream/exact output/statistical tolerance specified; null unspecified.",
    ),
    (
        "Exactly two different entries sum to target. Same entry cannot be reused, two equal durations at different positions allowed. Read-only. Fewer than two false. Optimize time over memory; O(n)/O(n).",
        "Null, negative/zero duration domain, numeric bounds and overflow unspecified.",
    ),
    (
        "One-based k from tail; return original node identity, no mutation/copy. Nonempty finite list in examples/reference. k=1 tail, k=length head; invalid k reference ArgumentOutOfRangeException. O(n)/O(1); one pass not required.",
        "Empty/null and cyclic input unspecified; recursion O(n) stack misses space goal.",
    ),
    (
        "MaxStack Push/Pop/GetMax integers, built-in Stack restriction. LIFO occurrences, getter non-consuming, repeated maxima survive one pop. Empty Pop/Peek reference InvalidOperationException. O(1) each/O(m) operations bound.",
        "Capacity/concurrency/exception message unspecified.",
    ),
    (
        "Unordered coin combinations, unlimited repetition; nonnegative target and positive denominations presumed. Read-only reference. Zero target one even no denominations; impossible/empty positive zero; oversized coin contributes none. O(A*d)/O(A).",
        "Repeated denomination entries unresolved (old reference separate passes); negative/zero domain undefined. Count overflow unspecified; final method name observed not independently mandated.",
    ),
    (
        "Two already nondecreasing arrays, preserve all occurrences, no deduplication. New result, inputs unchanged. Empty either/both permitted. O(m+n) time/result space.",
        "Null/unsorted outside specified domain; intermediate names differ, final MergeArrays.",
    ),
    (
        "Unsorted integer Meeting intervals StartTime/EndTime; condensed ascending union, merge touching boundaries. New list/new Meeting objects, preserve original order/fields. Nesting/duplicates/chains valid; singleton new object. O(n log n)/O(n); sorted case O(n).",
        "Empty old reference indexes first; not deliberate required failure. Null/reversed/zero duration unspecified, numeric overflow/range conversion unspecified.",
    ),
    (
        "Unweighted map string->string[]; any minimum-edge route including endpoints; null unreachable; start=end existing gives singleton. Endpoint missing reference ArgumentException. Cycles terminate, map read-only/new route. Context undirected, reference follows supplied directions; neighbor keys assumed. O(V+E)/O(V).",
        "Nulls, missing non-endpoint keys, asymmetric maps unspecified; no tied-route/neighbor-order mandate.",
    ),
    (
        "Original task storage-efficiency design; observed Trie.AddWord runnable adapter returns true first exact insertion, false repeat. Stateful sharing, prefixes not implicitly complete keys, empty reference new once. No URL normalization/network/casefolding. O(L) compatible, prefix-saving input-dependent.",
        "No deletion/lookup API specified. NUL collides with reference marker but not meaningful specified URL. Null unspecified; observed adapter must be labeled.",
    ),
    (
        "Given valid opener index, return matching closer index respecting nesting; other chars ignored, no mutation/substrings. C# UTF-16 positions. No closer reference ArgumentException. O(n)/O(1).",
        "Null/out-of-range/non-opener index validation unspecified; no quote/escape parser semantics.",
    ),
    (
        "Lowercase string, all occurrences reordered, no insertion/removal/normalization. Empty/single reference true. Not necessarily originally palindrome. O(n)/O(k), fixed alphabet constant.",
        "Lowercase Unicode repertoire unspecified, no casefold/ignore punctuation/null/normalization; reference char units not graphemes.",
    ),
    (
        "Each result position product of all others, same length; division forbidden, negatives/zeros/multiple zeros valid. Reference new array, inputs unchanged, fewer than two ArgumentException. O(n), one extra n-array only.",
        "Mutation not independently specified beyond reference; null/overflow unspecified.",
    ),
    (
        "Axis-parallel lower-left int rectangles, positive-area common region. Containment/identical valid. Edge/point contact no overlap. Reference new output/nonmutating and all-zero nonnull sentinel. O(1)/O(1).",
        "Question allows reasonable no-overlap handling; zero sentinel is reference choice. Negative dimensions/null/overflow unspecified. Zero dimensions reference no-overlap.",
    ),
    (
        "Set of all distinct character permutations, order irrelevant. Recursion required, loops allowed. Initial domain unique characters; reference set dedups repeats. Empty singleton empty string; singleton input itself. No optimization target.",
        "Repeated chars outside initial domain though reference handles them; null/Unicode grapheme/surrogate unspecified.",
    ),
    (
        "Reverse finite linked list in-place, existing objects reused, values remain on objects, old head becomes tail Next null. Return new head. Empty null, singleton same object. O(n)/O(1).",
        "Cyclic input unspecified.",
    ),
    (
        "Void mutation of provided char array, reverse elements, same identity/length. Empty/single unchanged. O(n)/O(1).",
        "Null/grapheme/surrogate semantics unspecified; C# char elements API.",
    ),
    (
        "Void in-place word-order reversal, preserve within-word spelling, same char array identity/length. Letters/spaces with one separator, unequal word lengths; empty/single reference unchanged. O(n)/O(1).",
        "Leading/trailing/repeated spaces, null, other whitespace, graphemes unspecified.",
    ),
    (
        "Rand5 no parameters, use supplied uniform Rand7 1..7 only; output uniform 1..5, range alone insufficient. O(1) space, unbounded worst-case source draws explicitly allowed.",
        "No injection/seed/stream/statistical threshold; source-draw independence implicit model.",
    ),
    (
        "Rand7 no parameters, use supplied uniform Rand5 1..5 only; output uniform 1..7. Two calls per attempt suffice optimized goal, not three. O(1) space, unbounded worst-case runtime allowed.",
        "No injection/seed/stream/statistical threshold; source-draw independence implicit.",
    ),
    (
        "TempTracker Insert 0..110, nullable GetMin/Max/Mean/Mode in final reference. State retains all readings; getters non-consuming. Any tied mode accepted. Empty final getters null, mean floating. O(1) operations/fixed-domain space.",
        "Question describes nonnullable getters but final code nullable. Invalid temp/overflow/mean tolerance unspecified.",
    ),
    (
        "Unlimited whole CakeType items, nonnegative int Weight/long Value/capacity, maximize value under capacity, unused space permitted. Read-only. Zero-weight positive value unbounded even capacity zero; reference InfinityException. Zero-zero no effect, empty/zero bounded capacity 0. O(t*k)/O(k).",
        "Constructor reference narrows int despite long property; preserve long capability. Cross-language infinite wire unspecified; null/negative outside domain/long overflow unspecified.",
    ),
    (
        "Unordered positive int IDs, exactly one once, every other twice; not consecutive/sorted/compact. Return unique value, no mutation. Singleton valid. O(n)/O(1).",
        "Empty/null/multiplicity violations unspecified; do not require incidental invalid behavior.",
    ),
    (
        "Scores in 0..K; descending output preserves multiplicity. Reference new array/nonmutation, empty/single supported. O(n+K) time/space incl result, O(n) when K fixed.",
        "No independent no-mutation restriction beyond reference; null/negative K/out-of-range unspecified.",
    ),
    (
        "Length n+1, every 1..n present once except sole twice, n>=1. Return sole duplicate, read-only. Minimal [1,1], short ref ArgumentException. O(n)/O(1).",
        "Null/invalid multiplicities unspecified. int sum intermediate overflow is incidental, not mandate; numeric bounds absent.",
    ),
    (
        "WordCloudData constructor/property dictionary counts tokens, input unchanged, order irrelevant. Sensible case aggregation and hyphenation/punctuation considered; policy deliberately flexible. Reference lowercase+initial capital merge, retain capital if no lowercase; internal apostrophes/letter-surrounded hyphens. Empty {}. One input traversal/O(n), dictionary only growing structure.",
        "Exact lexical/case policy intentionally unresolved. All-uppercase/mixed/locale/Unicode/apostrophe boundaries/whitespace not complete; ad hoc reference punctuation not authoritative; null/count overflow unspecified.",
    ),
]
assert len(facts) == len(S) == 41
records = []
for index, (spec, (verified, uncertainty)) in enumerate(zip(S, facts)):
    records.append(
        {
            "id": spec["sourceId"],
            "title": spec["title"],
            "sourceUrl": spec["sourceUrl"],
            "transferBatch": index // 6 + 1,
            "verifiedTechnicalFacts": verified,
            "uncertainties": uncertainty,
            "bankConventions": spec["bankConventions"],
        }
    )
doc = {
    "schemaVersion": 1,
    "archiveSha256": "aa6eb202de3cb17f7c034e2c86723005646908be774843da181acfd53b62d787",
    "inspection": "Read-only static HTML parsing of the user-supplied archive; no archived scripts or programs executed.",
    "transferBatchesComplete": list(range(1, 8)),
    "interpretation": [
        "Normalized technical facts from all 41 complete records in seven transfer batches; source expression and solution implementations excluded.",
        "A reference observation is not automatically a mandatory task rule.",
        "Bounded valid domains and deterministic bank adapters are disclosed separately.",
        "No private archive paths are retained.",
    ],
    "questions": records,
}
p = ROOT / "interviewcake/provenance/contracts.json"
p.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8", newline="\n")
print(
    len(records),
    "unique contracts",
    len({r["id"] for r in records}),
    "batches",
    doc["transferBatchesComplete"],
    "sha256",
    hashlib.sha256(p.read_bytes()).hexdigest(),
)
