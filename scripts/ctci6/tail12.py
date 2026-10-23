"""Independent file-tail exercise; public author-linked C++ code establishes task."""
SPEC=dict(ref='12.1',method='LastKLines',params=[('filePath','s'),('k','i')],result='strings',mutation='none',
 description='Read the text file at filePath and return its last k lines in their original order. If it contains fewer than k lines, return every line. Return line contents without their line terminators; an empty line is a real line, not end of file. Preserve the file. This callable returns the lines instead of printing them so the judge can compare the requested output.',
 constraints=['k is an integer in 1..1000. The judge supplies an existing readable file containing 0..20000 lines. Each line contains 0..128 printable ASCII characters (codes 32..126), followed by LF. The empty file contains zero lines. The final LF terminates the last line; it does not create an additional empty line. File opening and reading succeed for admitted inputs.', 'The first JSON argument is an array of line contents. The judge writes those lines to an actual temporary file and passes its path to LastKLines; your callable receives a path string, not that array. The second argument is k. Do not change or remove the file, and close any stream you open before returning.', 'Process the file sequentially, retaining at most k complete lines plus bounded read buffers and one current line. Do not load the entire file. Return a concrete sequence of strings. The return sequence may use O(k) references; returned character storage depends on the retained line lengths.'],
 why='A line can only belong to the final answer until k later lines arrive. Keeping a bounded queue therefore discards exactly the lines that have become too old. It avoids reading the whole file into memory and handles files shorter than k without padding. The final queue already has the required chronological order.',
 correctness='After processing t lines, the queue contains exactly the last min(t,k) processed lines in their original order. Initially this is true for the empty queue. Append the next line; if there are now k+1 entries, removing the oldest leaves exactly the most recent k. Otherwise all processed lines still fit. This proves the invariant by induction. At end of file, the queue is the required suffix. Testing the read operation for EOF rather than testing whether its string is empty preserves empty lines. No write operation is performed on the input file.',
 walkthrough='For a file with lines [north,"",east,west,south] and k=3, the queue evolves [north], [north,""], [north,"",east], ["",east,west], then [east,west,south]. The fourth and fifth reads discard only the oldest retained line. The output is [east,west,south]. For a file containing one blank line, the result is [""]; an empty file returns [].',
 example=([['north','','east','west','south'],3],['east','west','south']),
 time='O(N + C) time, where N is the number of lines and C is the number of file characters read. Each line enters and leaves the bounded queue at most once; constructing the result touches at most k entries.',
 space='O(k + S + B) space, where S is the total character storage of the retained lines and B is the fixed read buffer plus one line being assembled. With the admitted 128-character line limit this is O(k) auxiliary/output storage. The entire file is never retained.',
 edges=['Empty file, one blank line, blank lines within the final suffix, and whitespace-only lines.','k=1, k larger than the line count, exactly k lines, and multiple circular-buffer wraps.','20000 lines, maximum line length, punctuation and case preserved exactly; file contents preserved.'],
 related='The author-linked C++ print_k_lines implementation establishes sequential last-k file output; the independent course index identifies it as 12.1. Its stopping-on-empty-line behavior is not adopted: this bank explicitly treats blank lines as lines and uses actual EOF. All five independent implementations retain a bounded suffix and close their streams.',
 languageWhy={
 'csharp':'C# File.ReadLines reads lazily. Queue<string> retains the suffix, and foreach disposes its enumerator, closing the file before ToList returns the concrete result.',
 'java':'Java BufferedReader reads one line at a time. ArrayDeque removes its oldest entry in constant amortized time; try-with-resources closes the reader even if a read fails. The admitted inputs guarantee successful I/O; an unexpected IOException is reported rather than silently returning a partial suffix.',
 'cpp':'C++ std::getline distinguishes a successfully read empty line from EOF. std::deque supports constant-time removal at the front; the local ifstream closes through RAII when the method returns.',
 'python':'Python iterates an open file inside a with block and strips exactly the terminating LF from each admitted line. deque(maxlen=k) automatically discards the oldest entry. list materializes the final suffix before the context closes.',
 'javascript':'JavaScript uses synchronous readSync with a fixed 4096-byte buffer, not readFileSync. Printable ASCII makes byte-to-character decoding unambiguous. A k-slot circular array overwrites the oldest line; the output starts at the oldest retained slot. finally closes the descriptor, including unexpected failures.'})
EXTRA={
'csharp':'', 'java':'',
'cpp':'#include <fstream>\n#include <deque>\n#include <filesystem>\n', 'python':'from collections import deque\n', 'javascript':"const tailFs = require('node:fs');\n"}
BODIES={
'csharp':'''var suffix = new Queue<string>();
foreach (string line in System.IO.File.ReadLines(filePath)) {
    suffix.Enqueue(line);
    if (suffix.Count > k) suffix.Dequeue();
}
return new List<string>(suffix);''',
'java':'''var suffix = new ArrayDeque<String>();
try (var reader = new java.io.BufferedReader(new java.io.InputStreamReader(new java.io.FileInputStream(filePath), java.nio.charset.StandardCharsets.US_ASCII))) {
    String line;
    while ((line = reader.readLine()) != null) {
        suffix.addLast(line);
        if (suffix.size() > k) suffix.removeFirst();
    }
} catch (java.io.IOException error) {
    throw new java.io.UncheckedIOException(error);
}
return new ArrayList<>(suffix);''',
'cpp':'''std::ifstream input(filePath);
if (!input) throw std::runtime_error("Could not open input file");
std::deque<std::string> suffix;
std::string line;
while (std::getline(input, line)) {
    suffix.push_back(line);
    if (suffix.size() > static_cast<std::size_t>(k)) suffix.pop_front();
}
if (input.bad()) throw std::runtime_error("Could not read input file");
return std::vector<std::string>(suffix.begin(), suffix.end());''',
'python':'''suffix = deque(maxlen=k)
with open(filePath, "r", encoding="ascii", newline="") as source:
    for line in source:
        suffix.append(line[:-1])
return list(suffix)''',
'javascript':'''const descriptor = tailFs.openSync(filePath, "r");
const chunk = Buffer.alloc(4096), ring = new Array(k);
let used = 0, next = 0, current = "";
try {
    for (;;) {
        const count = tailFs.readSync(descriptor, chunk, 0, chunk.length, null);
        if (count === 0) break;
        for (let i = 0; i < count; ++i) {
            if (chunk[i] === 10) {
                ring[next] = current;
                next = (next + 1) % k;
                used = Math.min(used + 1, k);
                current = "";
            } else current += String.fromCharCode(chunk[i]);
        }
    }
} finally { tailFs.closeSync(descriptor); }
const result = [];
for (let i = 0; i < used; ++i) result.push(ring[(next - used + k + i) % k]);
return result;'''}

def oracle(reference,args):return args[0][-args[1]:]
def cases(spec):
    import itertools,json,random
    args=[spec['example'][0]]
    for n in range(5):
        for lines in itertools.product(('','A',' a '),repeat=n):
            for k in (1,2,3,7):args.append([list(lines),k])
    rng=random.Random(1201)
    for _ in range(40):args.append([[''.join(rng.choice(' abAZ09!~') for _ in range(rng.randrange(129))) for i in range(rng.randrange(100))],rng.randrange(1,35)])
    for n in (999,1000,1001,20000):
        for k in (1,999,1000):args.append([[str(i)+('x'*100 if i%2 else '') for i in range(n)],k])
    return [dict(arguments=a,expected=oracle('12.1',a)) for a in {json.dumps(a):a for a in args}.values()]
