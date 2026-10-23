"""Independent first recursion/dynamic-programming contracts; not the full chapter."""

SPECS = [
    dict(
        ref="8.1",
        method="CountTripleSteps",
        params=[("steps", "i")],
        result="i",
        mutation="none",
        description="Count the ordered sequences of hops that climb exactly steps stairs when each hop has size 1, 2 or 3. Sequences with the same hop sizes in different orders count separately. Return the exact integer count.",
        constraints=[
            "steps is a signed 32-bit integer no greater than 36. For a negative value return zero. For zero return one, representing the empty sequence. The upper bound keeps the exact result within signed 32-bit range.",
            "Preserve inputs. This exercise asks for a count, not an enumeration or the minimum number of hops.",
        ],
        why="Every nonempty route has a unique last hop, so routes divide into three disjoint groups by that hop. Their preceding routes climb one, two or three fewer stairs. Only those three preceding counts affect the next count, so older counts can be discarded.",
        correctness="Let W(n) be the required count, with W(0)=1 and W(n)=0 for n<0. Removing a route's last hop gives exactly one route counted by W(n-1), W(n-2) or W(n-3), and appending that hop reverses the mapping. Thus W(n) is their sum with no overlap or omission. Before each loop iteration, the three stored counts represent precisely those three preceding arguments. Updating them after the sum preserves the invariant and returns W(steps). Negative inputs are rejected before iteration.",
        walkthrough="For four stairs, the counts W(0)..W(4) are 1,1,2,4,7. The final value is W(3)+W(2)+W(1)=4+2+1. For example [1,3] and [3,1] are distinct routes; treating hop sizes as an unordered coin combination would undercount.",
        example=([4], 7),
        time="O(steps) time for nonnegative steps, with constant time for negative inputs.",
        space="O(1) auxiliary space: three preceding counts and a temporary sum.",
        edges=[
            "Negative signed endpoint, zero and one stair.",
            "Three-hop routes must not be confused with two-hop stair problems.",
            "The largest admitted steps value, 36, still fits the signed result type.",
        ],
        related="A staircase problem allowing only hops of size one or two has a different recurrence and cannot be substituted.",
    ),
    dict(
        ref="8.5",
        method="RecursiveMultiply",
        params=[("first", "i"), ("second", "i")],
        result="i",
        mutation="none",
        description="Compute first times second recursively using addition and bit operations instead of a multiplication operation. Halve the smaller operand to reduce recursive work; preserve the exact nonnegative result.",
        constraints=[
            "0 <= first,second <= 46340, so the product fits signed 32-bit range. Zero is admitted explicitly and returns zero, matching the public helper's zero base case.",
            "Do not use multiplication or division operators, a multiplication library, repeated addition proportional to the larger operand, or conversion to a representation that delegates multiplication. Addition, subtraction, shifts, bit tests, comparisons and recursion are allowed; a parity remainder test is also allowed. Preserve inputs.",
        ],
        why="If the smaller operand is 2q, its product is twice q times the larger operand. If it is 2q+1, add one more larger operand. Computing the half product once avoids branching into two independent recursive multiplications, and choosing the smaller operand bounds recursion by its bit length.",
        correctness="Zero gives the specified product immediately. For a positive smaller operand s, the recursive call receives floor(s/2), which is smaller and therefore terminates. By induction it returns floor(s/2) times the larger operand. Adding that value to itself and adding one larger operand exactly when s is odd gives s times that operand. Reordering the two original operands preserves multiplication, so this is the original requested product. All intermediate sums are nonnegative and no greater than the admitted final product.",
        walkthrough="For 7 and 12, recursively compute the product for 3 and 12, then for 1 and 12, then zero. Unwinding gives 12, then 12+12+12=36, then 36+36+12=84. Each half product is computed once, rather than multiplying both halves independently.",
        example=([7, 12], 84),
        time="O(log(s+1)) recursive calls and additions, where s is the smaller operand; zero takes constant time.",
        space="O(log(s+1)) recursion stack space, with no memo table or operand-sized sequence.",
        edges=[
            "Either operand zero; either operand one.",
            "Odd and even smaller operands, reversed argument order.",
            "Both operands at the admitted maximum and highly unequal operands.",
        ],
        related="A generic multiplication callable without the recursive operation restrictions is not an exact replacement.",
    ),
    dict(
        ref="8.11",
        method="CountCoinCombinations",
        params=[("amount", "i")],
        result="i",
        mutation="none",
        description="Count the unordered combinations of US coin denominations 1, 5, 10 and 25 cents that sum exactly to amount. Each denomination is available without limit. A combination is determined by its four coin counts; rearranging the same coins does not make a new combination.",
        constraints=[
            "0 <= amount <= 10000 cents. Return the exact signed 32-bit count. Amount zero has one combination: using no coins.",
            "Denominations are fixed by this exercise, not supplied as another argument. Preserve inputs. This asks for the number of combinations, not the fewest coins or ordered sequences.",
        ],
        why="Process denominations one at a time so each combination acquires one canonical construction order. When adding a denomination, reusing the newly updated smaller amount permits any number of that coin. Reversing the nesting to process amounts before coins would count multiple orders of the same collection.",
        correctness="Before processing a coin c, ways[a] counts combinations of a using only earlier denominations. During the increasing amount pass, the old ways[a] counts combinations using no c, while ways[a-c] already counts combinations using earlier coins and any number of c. Appending one c bijectively produces the combinations of a using at least one c. These two groups are disjoint and exhaustive. Initial ways[0]=1 gives the empty combination, and all other entries start at zero. After all four denominations, ways[amount] is the requested count.",
        walkthrough="For 10 cents there are four combinations: ten pennies; one nickel and five pennies; two nickels; or one dime. The nickel pass extends ways[5] into ways[10], allowing two nickels. Neither the order of the pennies nor placing a nickel before versus after them creates another combination.",
        example=([10], 4),
        time="O(d*amount) time for d=4 fixed denominations, hence O(amount).",
        space="O(amount) auxiliary storage for the amount-indexed count array.",
        edges=[
            "Zero and amounts below the smallest non-penny denomination.",
            "Exact denomination boundaries and combinations using repeated coins.",
            "The upper amount bound; exact counts remain within signed 32-bit range.",
        ],
        related="Minimum-coin change and ordered coin-sequence counting have different objectives and recurrences.",
    ),
]

SPECS += [
    dict(
        ref="8.4",
        method="PowerSet",
        params=[("values", "ai")],
        result="sets",
        mutation="none",
        description="Return every subset of the set represented by values, including the empty set and the entire set, exactly once. Return a collection of integer collections. The outer order and the element order inside each subset are unrestricted.",
        constraints=[
            "values contains 0..12 distinct signed 32-bit integers. Equal values are not admitted; each input element represents one set member.",
            "Do not modify the input. Every returned subset must contain only input members, with no repeated member. Different orders of the same members are the same subset, not different answers. For an empty input return one empty subset, not an empty outer collection.",
            "Examples show one deterministic valid ordering; the judge accepts all valid orders.",
        ],
        why="When a new set member arrives, every resulting subset either excludes it or includes it. Keep the existing subsets for the first group and make one independent copy with the new member appended for the second group. Snapshot the old subset count so newly created subsets are not processed again in that same pass.",
        correctness="Initially the result contains precisely the empty set, all subsets of zero processed members. Inductively, existing subsets are exactly the subsets that exclude the next distinct member. Appending that member to a copy of each old subset gives exactly those that include it. The groups are disjoint, and the copy mapping is one-to-one, so no subset is omitted or repeated. Copying before appending preserves the old subsets and the original input.",
        walkthrough="Starting with [[]], process 3 to obtain [[],[3]]. Then process 1: keep those two subsets and append independent copies [1] and [3,1]. All four subsets appear once. Appending to the original [3] object instead of a copy would corrupt an already completed subset.",
        example=([[3, 1]], [[], [3], [1], [3, 1]]),
        time="O(n*2^n) time to construct the output for n distinct members.",
        space="O(n*2^n) total returned storage; each copied subset has at most n members. No recursive stack is used.",
        edges=[
            "Empty input and one member.",
            "Negative and extreme signed values; input order need not be sorted.",
            "All 4096 subsets at the admitted maximum size, without duplicates or input mutation.",
        ],
        related="Existing subset algorithms require a domain/order/mutation comparison before aliasing; this reference retains its own explicit set-valued grading contract.",
    ),
    dict(
        ref="8.7",
        method="PermutationsDistinct",
        params=[("text", "s")],
        result="strings",
        mutation="none",
        description="Return every permutation of text exactly once. Input characters are all distinct, so different choices of which character occupies a position produce different strings. Output order is unrestricted.",
        constraints=[
            "text contains 0..8 distinct lowercase ASCII English letters a..z. It is nonnull. Preserve the input.",
            "Return one empty string for the empty input. Every result has the same length and characters as text; there must be no repeated result. Examples display one valid ordering, and any output order is accepted.",
        ],
        why="Fix one output position at a time. Swap each remaining character into that position, recursively arrange the suffix, then undo the swap. Distinct characters make these branches disjoint, so no deduplication set is needed.",
        correctness="At recursion depth d, the prefix contains d distinct chosen input characters and the remaining suffix contains exactly the unchosen ones. Swapping each suffix position into d enumerates every possible next character once. Induction on remaining length therefore gives every arrangement of the suffix once for each unique prefix. At full depth, copying the character buffer captures one completed permutation. Restoring the swap preserves the parent state for the next branch.",
        walkthrough="For ab, fix a first and emit ab; undo that choice, fix b first and emit ba. For abc, the a-first branch emits abc and acb before the b-first and c-first branches. Restoring swaps is what lets each later branch start from the correct unchosen characters.",
        example=(["ab"], ["ab", "ba"]),
        time="O(n*n!) time including construction of every length-n output string.",
        space="O(n) workspace and recursion depth, excluding O(n*n!) returned character storage.",
        edges=[
            "Empty text gives one empty permutation.",
            "One character and unsorted distinct input.",
            "Length eight produces all 40320 distinct outputs.",
        ],
        related="The duplicate-aware permutation exercise has different branching and uniqueness requirements and is retained separately.",
    ),
    dict(
        ref="8.8",
        method="PermutationsWithDuplicates",
        params=[("text", "s")],
        result="strings",
        mutation="none",
        description="Return every DISTINCT permutation of text exactly once, even when equal characters occur multiple times. Equal copies of a letter are indistinguishable. Output order is unrestricted.",
        constraints=[
            "text contains 0..8 lowercase ASCII English letters a..z and is nonnull. Repeated letters are allowed; all-distinct input is also valid. Preserve the input.",
            "Every result uses each letter exactly as many times as text. Return one empty string for empty input. Returning duplicate strings and relying on the caller to deduplicate is incorrect.",
        ],
        why="Choose the next letter by its remaining frequency, rather than by the identity of one equal input occurrence. This combines equal-occurrence branches before they generate duplicate strings. Decrement before descent and restore afterward so sibling branches see the original remaining counts.",
        correctness="At depth d, the character counts describe exactly the multiset not yet placed in the output prefix. A branch exists once for each letter with a positive remaining count and consumes exactly one copy. Thus every emitted string has the required multiplicities. Any valid permutation has a unique next letter at each depth, so it follows exactly one branch sequence and is emitted once. Restoring each count maintains the invariant for later choices.",
        walkthrough="For aab, the first choice is a or b, not first-a versus second-a. Choosing a leaves counts a:1,b:1 and yields aab or aba; choosing b leaves a:2 and yields baa. Three strings are returned, rather than six occurrence-labeled branches containing duplicates.",
        example=(["aab"], ["aab", "aba", "baa"]),
        time="O(26*n*U), hence O(n*U) for this fixed alphabet, where U=n! divided by the product of each letter-count factorial. The bound includes prefix traversal and copied output strings.",
        space="O(n+26) workspace/recursion storage, excluding O(n*U) returned character storage.",
        edges=[
            "All letters equal, mixed multiplicities and all-distinct text.",
            "Empty text and the maximum input length.",
            "Repeated outputs or missing multiplicities are rejected irrespective of output order.",
        ],
        related="The distinct-character permutation exercise cannot simply enumerate occurrence permutations without duplicate-aware branching.",
    ),
    dict(
        ref="8.9",
        method="GenerateParentheses",
        params=[("pairs", "i")],
        result="strings",
        mutation="none",
        description="Return every balanced string containing exactly pairs opening parentheses and pairs closing parentheses, exactly once. Output order is unrestricted. A prefix must never contain more closing than opening parentheses.",
        constraints=[
            "0 <= pairs <= 8. Only the two characters ( and ) are used. Return one empty string for zero pairs.",
            "Every output has length 2*pairs and is properly balanced, and there are no repeated outputs. This is generation of all strings, not a count or validation of one supplied string.",
        ],
        why="Construct only prefixes that can still become balanced. Add an opening parenthesis while some remain; add a closing one only when it closes an already-open unmatched parenthesis. Pruning invalid prefixes prevents generating arbitrary strings just to reject them afterward.",
        correctness="The recursion tracks numbers opened and closed. Its rules maintain 0 <= closed <= opened <= pairs, so no generated prefix is invalid. Reaching 2*pairs characters forces both counts to equal pairs and yields a balanced string. Conversely, every balanced string obeys these same prefix bounds, so its next character is an available branch at every depth. It is therefore generated exactly once along its unique character-choice path.",
        walkthrough="For two pairs, start with (. The next opening choice leads to (( and then (()), while the next closing choice leads to () and then ()(). Starting with ) is never explored because it would close nothing. The two results are (()) and ()().",
        example=([2], ["(())", "()()"]),
        time="O(p*C_p) time including copying outputs, where C_p is the number of balanced strings with p pairs (the pth Catalan number).",
        space="O(p) buffer/recursion workspace, excluding O(p*C_p) returned characters.",
        edges=[
            "Zero and one pair.",
            "Nesting and adjacent groups must both appear.",
            "Eight pairs yields 1430 unique balanced strings; prefixes that close too early are invalid.",
        ],
        related="A parentheses validator or a Catalan-number counter does not generate the required collection of strings.",
    ),
]
SPECS.sort(key=lambda spec: tuple(map(int, spec["ref"].split("."))))

for _spec in SPECS:
    if _spec["ref"] in ("8.4", "8.7", "8.8", "8.9"):
        _spec["constraints"].append(
            "Return the concrete lists/vectors in the selected callable signature: a List in C#/Java, an Array in JavaScript, a list in Python, or a vector in C++. A generator or iterator alone is not the return value. "
        )

for _spec in SPECS:
    if _spec["ref"] == "8.4":
        _spec["constraints"].append(
            "Each returned subset is a concrete integer list/vector as well; both levels must be materialized."
        )
