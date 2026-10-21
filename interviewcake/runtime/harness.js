'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { performance } = require('node:perf_hooks');
// CONFIGURATION
const exported = require('./solution.js');
const { LinkedListNode, BinaryTreeNode, GraphNode, Meeting, Rectangle, CakeType, InfinityException, RandomSource } = exported;
class ContractError extends Error {}
class NeedChoice extends Error {
  constructor(lower, upper) { super('An injected random choice is required.'); this.Lower = lower; this.Upper = upper; }
}
function check(condition, message = 'The result violates the bank contract.') {
  if (!condition) throw new ContractError(message);
}
function fresh() { return new exported[ClassName](); }
function call(instance, name, ...args) {
  if (typeof instance[name] !== 'function') throw new Error('Missing method ' + name);
  return instance[name](...args);
}
function load(value, kind) {
  switch (kind) {
    case 'tree': {
      if (!value.length || value[0] === null) return null;
      const root = new BinaryTreeNode(value[0]), queue = [root]; let position = 1;
      for (let i = 0; i < queue.length; i++) for (const child of ['Left', 'Right']) {
        if (position < value.length && value[position] !== null) { queue[i][child] = new BinaryTreeNode(value[position]); queue.push(queue[i][child]); }
        position++;
      }
      return root;
    }
    case 'list': {
      let head = null; for (let i = value.length - 1; i >= 0; i--) head = new LinkedListNode(value[i], head); return head;
    }
    case 'graph': {
      const nodes = value.map((_, i) => new GraphNode('v' + i));
      for (let i = 0; i < nodes.length; i++) for (const neighbor of value[i]) nodes[i].Neighbors.add(nodes[neighbor]);
      return nodes;
    }
    case 'meetings': return value.map(v => new Meeting(v[0], v[1]));
    case 'rect': return new Rectangle(...value);
    case 'cakes': return value.map(v => new CakeType(v[0], v[1]));
    case 'chars': return value.split('');
    case 'ai': case 'as': return value.slice();
    case 'map': return Object.fromEntries(Object.entries(value).map(([key, neighbors]) => [key, neighbors.slice()]));
    case 'i': case 'l': case 's': case 'files': return value;
    default: throw new Error('Unknown argument kind ' + kind);
  }
}
function listNodes(head) {
  const result = [], seen = new Set();
  while (head !== null) {
    check(head !== undefined && typeof head === 'object' && !seen.has(head), 'The list contains a cycle or an invalid node.');
    seen.add(head); result.push(head); head = head.Next;
  }
  return result;
}
function treeNodes(root) {
  const result = [], seen = new Set(), pending = root === null ? [] : [root];
  while (pending.length) {
    const node = pending.pop();
    check(node !== undefined && node !== null && typeof node === 'object' && !seen.has(node), 'Input must remain a tree.');
    seen.add(node); result.push(node);
    if (node.Left !== null) pending.push(node.Left);
    if (node.Right !== null) pending.push(node.Right);
  }
  return result;
}
function json(value) {
  return JSON.stringify(value, (key, item) => {
    if (typeof item === 'number' && !Number.isFinite(item)) throw new TypeError('Nonfinite result number.');
    if (['undefined', 'function', 'symbol'].includes(typeof item)) throw new TypeError('Unserializable result value.');
    return typeof item === 'bigint' ? JSON.rawJSON(item.toString()) : item;
  });
}
function dump(value, kind = '') {
  if (value === null) return null;
  switch (kind) {
    case 'tree': return treeNodes(value).map(node => [node.Value, node.Left?.Value ?? null, node.Right?.Value ?? null]);
    case 'list': return listNodes(value).map(node => node.Value);
    case 'meetings': check(Array.isArray(value)); return value.map(node => [node.StartTime, node.EndTime]);
    case 'rect': return [value.LeftX, value.BottomY, value.Width, value.Height];
    case 'cakes': return value.map(node => [node.Weight, node.Value]);
    case 'chars': return value.join('');
    case 'pairs': check(Array.isArray(value)); return value.map(pair => [pair.OriginalPath, pair.DuplicatePath]);
    case 'set': check(value instanceof Set, 'Return a set of distinct strings.'); return [...value];
    default: return value;
  }
}
function preserve(args) {
  const trees = [], lists = [], arrayObjects = [], mapArrays = [];
  for (let i = 0; i < args.length; i++) {
    const value = args[i], kind = Kinds[i];
    if (kind === 'tree') for (const node of treeNodes(value)) trees.push({ node, Value: node.Value, Left: node.Left, Right: node.Right });
    if (kind === 'list') for (const node of listNodes(value)) lists.push({ node, Value: node.Value, Next: node.Next });
    if (kind === 'meetings' || kind === 'cakes') arrayObjects.push({ array: value, nodes: value.slice() });
    if (kind === 'map') for (const [key, neighbors] of Object.entries(value)) mapArrays.push({ map: value, key, neighbors });
  }
  const before = args.map((value, i) => json(dump(value, Kinds[i])));
  return () => {
    check(trees.every(v => v.node.Value === v.Value && v.node.Left === v.Left && v.node.Right === v.Right), 'Tree values and links must remain unchanged.');
    check(lists.every(v => v.node.Value === v.Value && v.node.Next === v.Next), 'List values and links must remain unchanged.');
    check(arrayObjects.every(v => v.array.length === v.nodes.length && v.nodes.every((node, i) => v.array[i] === node)), 'Preserve the original element objects and ordering.');
    check(mapArrays.every(v => v.map[v.key] === v.neighbors), 'Preserve original neighbor-array objects.');
    check(args.every((value, i) => json(dump(value, Kinds[i])) === before[i]), 'Read-only input was modified.');
  };
}
function filesSnapshot(root) {
  const pending = [root], entries = [];
  while (pending.length) {
    const directory = pending.pop();
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const full = path.join(directory, entry.name), relative = path.relative(root, full);
      if (entry.isDirectory()) { entries.push('D:' + relative); pending.push(full); }
      else entries.push('F:' + relative + ':' + fs.statSync(full).mtimeMs + ':' + crypto.createHash('sha256').update(fs.readFileSync(full)).digest('hex'));
    }
  }
  return entries.sort().join('\n');
}
function state(raw) {
  const instance = fresh(), operations = raw[0], values = raw[1], output = []; let count = 0;
  for (let i = 0; i < operations.length; i++) {
    const method = operations[i];
    const empty = count === 0 && (Mode === 'queue' && method === 'Dequeue' || Mode === 'stack' && ['Pop', 'GetMax'].includes(method));
    try {
      const result = call(instance, method, ...values[i]);
      check(!empty, 'An empty-state operation must signal an error.'); output.push(result === undefined ? null : result);
    } catch (error) {
      if (empty && !(error instanceof ContractError) && !(error instanceof NeedChoice)) output.push({ error: 'empty' });
      else throw error;
    }
    if (['Enqueue', 'Push'].includes(method)) count++;
    else if (['Dequeue', 'Pop'].includes(method) && !empty) count--;
  }
  return output;
}
function randomCheck(raw) {
  const shuffle = Mode === 'shuffle', maximum = Mode === 'rand5' ? 7 : 5, outcomes = Mode === 'rand5' ? 5 : 7;
  const original = shuffle ? raw[0].slice() : [], probabilities = new Map(), pending = [{ prefix: [], weight: 1 }];
  let unresolved = 0, branches = 0;
  function sameElements(array) {
    check(Array.isArray(array) && array.length === original.length && json(array.slice().sort((a, b) => a - b)) === json(original.slice().sort((a, b) => a - b)), 'Shuffle changed element multiplicities.');
  }
  function bounds(lower, upper) {
    check(Number.isInteger(lower) && Number.isInteger(upper) && lower <= upper && (shuffle ? lower >= 0 && upper < Math.max(1, original.length) : lower === 1 && upper === maximum), 'Unexpected random-source bounds.');
  }
  while (pending.length) {
    const item = pending.pop(); check(++branches <= 100000, 'Randomized algorithm used too many decision branches.');
    let position = 0, draws = 0;
    RandomSource.Draw = (lower, upper) => {
      check(++draws <= 128, 'Randomized algorithm exceeded the draw budget.'); bounds(lower, upper);
      if (position >= item.prefix.length) throw new NeedChoice(lower, upper);
      const choice = item.prefix[position++]; check(choice >= lower && choice <= upper, 'Invalid injected choice.'); return choice;
    };
    const array = original.slice();
    try {
      let result = shuffle ? call(fresh(), Method, array) : call(fresh(), Method);
      if (shuffle) { sameElements(array); result = array.join(','); }
      else {
        check(draws > 0 && Number.isInteger(result) && result >= 1 && result <= outcomes, 'Use the supplied source and return an in-range die face.');
        if (Mode === 'rand7') check(draws % 2 === 0, 'Use two Rand5 draws per completed Rand7 attempt.');
      }
      const key = String(result); probabilities.set(key, (probabilities.get(key) ?? 0) + item.weight);
    } catch (error) {
      if (!(error instanceof NeedChoice)) throw error;
      const limit = shuffle ? Math.max(8, original.length * 2) : 8;
      if (item.prefix.length >= limit) { unresolved += item.weight; continue; }
      for (let choice = error.Lower; choice <= error.Upper; choice++)
        pending.push({ prefix: [...item.prefix, choice], weight: item.weight / (error.Upper - error.Lower + 1) });
    }
  }
  if (shuffle) {
    if (new Set(original).size === original.length && original.length <= 5) {
      let factorial = 1; for (let i = 2; i <= original.length; i++) factorial *= i;
      check(unresolved < 1e-10 && probabilities.size === factorial && [...probabilities.values()].every(p => Math.abs(p - 1 / factorial) < 1e-9), 'Shuffle is biased over complete permutations.');
    }
  } else {
    check(unresolved < 0.02, 'Rejection probability exceeds bounded judge exploration.');
    for (let i = 1; i <= outcomes; i++) {
      const probability = probabilities.get(String(i)) ?? 0;
      check(probability <= 1 / outcomes + 1e-9 && probability + unresolved >= 1 / outcomes - 1e-9, 'Die transformation is biased over injected choices.');
    }
  }
  let seed = 0x85ebca6b, seededInstance = null;
  const counts = Array(outcomes + 1).fill(0), samples = 4096, sequence = [];
  const distinctSmallShuffle = shuffle && original.length <= 5 && new Set(original).size === original.length;
  const permutationCounts = new Map(distinctSmallShuffle ? [...probabilities.keys()].map(key => [key, 0]) : []);
  for (let trial = 0; trial < samples; trial++) {
    let draws = 0, forcedPosition = 0;
    const forced = !shuffle && trial === 0 ? raw[0] : [];
    RandomSource.Draw = (lower, upper) => {
      check(++draws <= 128, 'Too many random draws.'); bounds(lower, upper);
      if (forcedPosition < forced.length) {
        const choice = forced[forcedPosition++]; check(Number.isInteger(choice) && choice >= lower && choice <= upper, 'Invalid supplied random prefix.'); return choice;
      }
      seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
      return lower + Math.floor(seed * (upper - lower + 1) / 4294967296);
    };
    const array = original.slice();
    if (seededInstance === null) seededInstance = fresh();
    const result = shuffle ? call(seededInstance, Method, array) : call(seededInstance, Method);
    if (shuffle) {
      sameElements(array); if (array.length > 1) check(draws > 0, 'Use the supplied random source.');
      if (distinctSmallShuffle) {
        const key = array.join(',');
        check(permutationCounts.has(key), 'Shuffle returned an unexpected permutation.');
        permutationCounts.set(key, permutationCounts.get(key) + 1);
      }
    }
    else {
      check(draws > 0 && Number.isInteger(result) && result >= 1 && result <= outcomes, 'Invalid die result/source usage.');
      if (Mode === 'rand7') check(draws % 2 === 0, 'Use two Rand5 draws per completed Rand7 attempt.');
      counts[result]++; sequence.push(result - 1);
    }
  }
  if (distinctSmallShuffle) {
    const expected = samples / permutationCounts.size;
    const chiSquare = [...permutationCounts.values()].reduce((sum, count) => sum + (count - expected) ** 2 / expected, 0);
    check(chiSquare <= 4 * (permutationCounts.size - 1) + 80, 'Repeated shuffles are biased over complete permutations.');
  }
  if (!shuffle) {
    const expected = samples / outcomes;
    check(counts.slice(1).reduce((sum, count) => sum + (count - expected) ** 2 / expected, 0) < 40, 'Seeded die distribution is biased.');
    const pairs = Array(outcomes ** 2).fill(0), triples = Array(outcomes ** 3).fill(0);
    for (let i = 1; i < sequence.length; i++) pairs[sequence[i - 1] * outcomes + sequence[i]]++;
    for (let i = 2; i < sequence.length; i++) triples[(sequence[i - 2] * outcomes + sequence[i - 1]) * outcomes + sequence[i]]++;
    function chiSquare(bins, total) {
      const expectedCount = total / bins.length;
      return bins.reduce((sum, count) => sum + (count - expectedCount) ** 2 / expectedCount, 0);
    }
    check(chiSquare(pairs, samples - 1) < 4 * (pairs.length - 1) + 80, 'Adjacent die outputs are correlated.');
    check(chiSquare(triples, samples - 2) < 4 * (triples.length - 1) + 80, 'Consecutive die triples are correlated.');
  }
  return true;
}
function execute(raw) {
  if (['queue', 'stack', 'trie', 'temperature'].includes(Mode)) return state(raw);
  if (Mode === 'wordcloud') {
    const words = new exported[ClassName](raw[0]).WordsToCounts;
    check(words !== null && typeof words === 'object' && [Object.prototype, null].includes(Object.getPrototypeOf(words)), 'WordsToCounts must be a plain dictionary.');
    check(Object.values(words).every(value => Number.isInteger(value)), 'Word counts must be integers.'); return words;
  }
  if (['shuffle', 'rand5', 'rand7'].includes(Mode)) return randomCheck(raw);
  if (Mode === 'cycle') {
    const head = load(raw[0], 'list'), nodes = listNodes(head), index = raw[1];
    if (index >= 0) nodes[nodes.length - 1].Next = nodes[index];
    const before = nodes.map(node => [node.Value, node.Next]), actual = call(fresh(), Method, head);
    check(nodes.every((node, i) => node.Value === before[i][0] && node.Next === before[i][1]), 'Cycle detection modified the list.'); return actual;
  }
  if (Mode === 'delete') {
    const head = load(raw[0], 'list'), nodes = listNodes(head), before = nodes.map(node => [node.Value, node.Next]), index = raw[1];
    call(fresh(), Method, nodes[index]);
    check(nodes.every((node, i) => { const expected = before[i === index ? index + 1 : i]; return node.Value === expected[0] && node.Next === expected[1]; }), 'Deletion violated target/successor alias semantics.');
    return dump(head, 'list');
  }
  if (Mode === 'reverse_list') {
    const head = load(raw[0], 'list'), nodes = listNodes(head), values = nodes.map(node => node.Value);
    const result = call(fresh(), Method, head), after = listNodes(result), reverse = nodes.slice().reverse();
    check(after.length === reverse.length && reverse.every((node, i) => after[i] === node && node.Next === (reverse[i + 1] ?? null)) && nodes.every((node, i) => node.Value === values[i]), 'Reversal must reuse the original nodes in reverse order.');
    return result === null ? [] : dump(result, 'list');
  }
  const args = Kinds.map((kind, i) => load(raw[i], kind));
  if (Mode === 'chars' || Mode === 'words') {
    const array = args[0]; call(fresh(), Method, ...args);
    check(array.length === raw[0].length && array.every(character => typeof character === 'string' && character.length === 1), 'Preserve the mutable character array and its length.'); return array.join('');
  }
  if (Mode === 'color') {
    const graph = args[0], nodes = graph.slice(), labels = nodes.map(node => node.Label), sets = nodes.map(node => node.Neighbors), edges = sets.map(neighbors => new Set(neighbors));
    const colors = args[1], palette = colors.slice(); call(fresh(), Method, ...args);
    check(graph.length === nodes.length && nodes.every((node, i) => graph[i] === node), 'Preserve the graph array and original node objects.');
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];
      check(node.Label === labels[i] && node.Neighbors === sets[i] && node.Neighbors instanceof Set && node.Neighbors.size === edges[i].size && [...edges[i]].every(neighbor => node.Neighbors.has(neighbor)), 'Preserve graph labels and original neighbor-set objects/edges.');
      check(node.Color !== null && palette.includes(node.Color) && [...node.Neighbors].every(neighbor => neighbor.Color !== node.Color), 'Adjacent nodes must receive different supplied colors.');
    }
    check(json(colors) === json(palette), 'The palette was modified.'); return true;
  }
  const verify = preserve(args), beforeFiles = Mode === 'files' ? filesSnapshot(args[0]) : null;
  let actual;
  try { actual = call(fresh(), Method, ...args); }
  catch (error) {
    if (!(error instanceof InfinityException)) throw error;
    verify(); return { error: 'infinite' };
  }
  verify();
  if (Mode === 'files') { check(filesSnapshot(args[0]) === beforeFiles, 'The filesystem must remain unchanged.'); return dump(actual, 'pairs'); }
  if (Mode === 'kth') {
    const index = listNodes(args[1]).indexOf(actual); check(index >= 0, 'Return an original node reference.'); return index;
  }
  if (Mode === 'meetings') check(Array.isArray(actual) && actual !== args[0] && actual.every(node => !args[0].includes(node)), 'Return new interval objects.');
  if (Mode === 'rect') check(actual instanceof Rectangle && !args.includes(actual), 'Return a new rectangle.');
  if (Result === 'ai') check(Array.isArray(actual) && !args.includes(actual), 'Return a newly allocated result array.');
  return dump(actual, Result);
}

const cases = JSON.parse(fs.readFileSync('cases.json', 'utf8')), results = [];
for (const raw of cases) {
  const started = performance.now(); let actual = null, error = null, validation = false;
  try {
    // Snapshot per-case results so a later method call cannot mutate a prior
    // answer, and one malformed/cyclic answer does not corrupt every result.
    actual = JSON.parse(json(execute(raw)));
  } catch (exception) {
    actual = null; validation = exception instanceof ContractError;
    error = String((validation ? '' : (exception.name ?? 'Error') + ': ') + exception.message).slice(0, 2000);
  }
  results.push({ Actual: actual, Error: error, ElapsedMs: performance.now() - started, ValidationFailed: validation });
}
fs.writeFileSync('results.json', json(results));
