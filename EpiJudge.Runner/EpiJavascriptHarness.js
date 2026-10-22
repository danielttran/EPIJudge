// Typed EPI submission protocol. Configuration values are JSON literals supplied
// by SubmissionRunner; no course runtime or external services are required.
const fs = require('node:fs');
const { performance } = require('node:perf_hooks');
const targetName = __TARGET_NAME__;
const problemId = __PROBLEM_ID__;
const argumentTypes = __ARGUMENT_TYPES_JSON__;
const resultType = __RESULT_TYPE__;

class JudgeValidationException extends Error {}
function check(condition, message = 'The result violates the problem contract.') {
  if (!condition) throw new JudgeValidationException(message);
}
class ListNode {
  constructor(data = 0, next = null) { this.data = data; this.next = next; }
}
class BinaryTreeNode {
  constructor(data = 0, left = null, right = null, parent = null) {
    this.data = data; this.left = left; this.right = right;
    this.parent = parent; this.next = null; this.size = 1;
  }
}
class PostingListNode {
  constructor(order = 0, next = null, jump = null) {
    this.order = order; this.next = next; this.jump = jump;
  }
}
class GraphVertex {
  constructor(label = 0) { this.label = label; this.edges = []; }
}
Object.assign(globalThis, { ListNode, BinaryTreeNode, PostingListNode, GraphVertex });

function losslessParse(text) {
  return JSON.parse(text, (key, value, context) =>
    typeof value === 'number' && !Number.isSafeInteger(value) &&
    /^-?\d+$/.test(context.source) ? BigInt(context.source) : value);
}
function stringify(value) {
  return JSON.stringify(value, (key, item) =>
    typeof item === 'bigint' ? JSON.rawJSON(item.toString()) : item);
}
function parts(grammar) {
  const inner = grammar.slice(grammar.indexOf('(') + 1, -1);
  let depth = 0, start = 0; const output = [];
  for (let i = 0; i < inner.length; i++) {
    if (inner[i] === '(') depth++;
    else if (inner[i] === ')') depth--;
    else if (inner[i] === ',' && depth === 0) { output.push(inner.slice(start, i).trim()); start = i + 1; }
  }
  output.push(inner.slice(start).trim()); return output;
}
function toList(values) {
  const dummy = new ListNode(); let tail = dummy;
  for (const value of values ?? []) { tail.next = new ListNode(value); tail = tail.next; }
  return dummy.next;
}
function toTree(values) {
  if (!values?.length || values[0] === null) return null;
  const root = new BinaryTreeNode(values[0]), queue = [root]; let position = 1;
  for (let i = 0; i < queue.length && position < values.length; i++) {
    const node = queue[i];
    for (const side of ['left', 'right']) {
      if (position < values.length && values[position] !== null) {
        node[side] = new BinaryTreeNode(values[position], null, null, node); queue.push(node[side]);
      }
      position++;
    }
  }
  for (let i = queue.length - 1; i >= 0; i--)
    queue[i].size = 1 + (queue[i].left?.size ?? 0) + (queue[i].right?.size ?? 0);
  return root;
}
function convert(value, grammar) {
  if (grammar === 'long') return typeof value === 'bigint' ? value : Number(value);
  if (grammar === 'int' || grammar === 'float') return Number(value);
  if (grammar === 'bool' || grammar === 'string' || !grammar) return value;
  const sub = parts(grammar);
  if (grammar.startsWith('array(')) return value.map(v => convert(v, sub[0]));
  if (grammar.startsWith('set(')) return new Set(value.map(v => convert(v, sub[0])));
  if (grammar.startsWith('tuple(')) return value.map((v, i) => convert(v, sub[i]));
  if (grammar.startsWith('linked_list(')) return toList(value.map(v => convert(v, sub[0])));
  if (grammar.startsWith('binary_tree(')) return toTree(value.map(v => v === null ? null : convert(v, sub[0])));
  throw new Error('Unsupported argument grammar: ' + grammar);
}
function listNodes(head, allowCycle = false) {
  const nodes = [], seen = new Set();
  while (head != null) {
    check(typeof head === 'object' && !Array.isArray(head), 'Return linked-list nodes, not a serialized array.');
    if (seen.has(head)) { check(allowCycle, 'The output list contains a cycle.'); break; }
    seen.add(head); nodes.push(head); head = head.next;
  }
  return nodes;
}
function treeNodes(root) {
  const nodes = [], seen = new Set(), stack = root == null ? [] : [root];
  while (stack.length) {
    const node = stack.pop();
    check(typeof node === 'object' && !Array.isArray(node), 'Return tree nodes, not a serialized array.');
    check(!seen.has(node), 'The tree contains a cycle or a shared child.');
    seen.add(node); nodes.push(node);
    if (node.right != null) stack.push(node.right);
    if (node.left != null) stack.push(node.left);
  }
  return nodes;
}
function inorder(root) {
  treeNodes(root); const values = [], stack = []; let node = root;
  while (node != null || stack.length) {
    while (node != null) { stack.push(node); node = node.left; }
    node = stack.pop(); values.push(node.data); node = node.right;
  }
  return values;
}
function treeValues(root) {
  treeNodes(root); if (root == null) return [];
  const values = [], queue = [root];
  for (let i = 0; i < queue.length; i++) {
    const node = queue[i];
    if (node == null) values.push(null);
    else { values.push(node.data); queue.push(node.left ?? null, node.right ?? null); }
  }
  while (values.length && values.at(-1) === null) values.pop();
  return values;
}
function serialize(value, grammar) {
  if (grammar.startsWith('linked_list(')) return listNodes(value).map(node => serialize(node.data, parts(grammar)[0]));
  if (grammar.startsWith('binary_tree(')) return treeValues(value).map(item => item === null ? null : serialize(item, parts(grammar)[0]));
  if (grammar.startsWith('array(') || grammar.startsWith('set(')) {
    check(Array.isArray(value) || value instanceof Set, 'Return the declared collection type.');
    return Array.from(value, item => serialize(item, parts(grammar)[0]));
  }
  if (grammar.startsWith('tuple(')) {
    const sub = parts(grammar); check(Array.isArray(value) && value.length === sub.length, 'Return a tuple with the declared arity.');
    return value.map((item, i) => serialize(item, sub[i]));
  }
  if (grammar === 'long') {
    check(typeof value === 'bigint' || typeof value === 'number' && Number.isInteger(value), 'Return an integer.');
    return value;
  }
  if (grammar === 'int') check(typeof value === 'number' && Number.isInteger(value), 'Return an integer.');
  else if (grammar === 'float') check(typeof value === 'number' && Number.isFinite(value), 'Return a finite number.');
  else if (grammar === 'bool') check(typeof value === 'boolean', 'Return a boolean.');
  else if (grammar === 'string') check(typeof value === 'string', 'Return a string.');
  else if (grammar === 'void') return true;
  else if (!grammar) return value;
  return value;
}
function same(left, right) {
  if (left.length !== right.length) return false;
  const counts = new Map();
  for (const value of left) { const k = stringify(value); counts.set(k, (counts.get(k) ?? 0) + 1); }
  for (const value of right) {
    const k = stringify(value), count = counts.get(k) ?? 0;
    if (!count) return false;
    if (count === 1) counts.delete(k); else counts.set(k, count - 1);
  }
  return counts.size === 0;
}
function equal(left, right) { return stringify(left) === stringify(right); }
function snapshotList(head) { return listNodes(head).map(node => ({ node, data: node.data, next: node.next })); }
function unchangedList(snapshot) {
  check(snapshot.every(item => item.node.data === item.data && item.node.next === item.next), 'Preserve the original input list.');
}
function snapshotTree(root) {
  return treeNodes(root).map(node => ({ node, data: node.data, left: node.left, right: node.right, parent: node.parent }));
}
function unchangedTree(snapshot) {
  check(snapshot.every(item => item.node.data === item.data && item.node.left === item.left && item.node.right === item.right && item.node.parent === item.parent), 'Preserve the original input tree.');
}

// Redirect submission prints without hiding the judge's final protocol output.
const writeOutput = process.stdout.write.bind(process.stdout);
process.stdout.write = () => true;
let mod, moduleError;
try { mod = require('./solution.js'); } catch (error) { moduleError = error; }
function context() {
  let instance;
  function resolve(name) {
    if (moduleError) throw moduleError;
    if (mod && typeof mod[name] === 'function') return mod[name].bind(mod);
    if (typeof mod === 'function') {
      if (mod.prototype && typeof mod.prototype[name] === 'function') {
        instance ??= new mod(); return instance[name].bind(instance);
      }
      return mod;
    }
    if (mod && typeof mod.Solution === 'function') {
      instance ??= new mod.Solution();
      if (typeof instance[name] === 'function') return instance[name].bind(instance);
    }
    if (typeof globalThis[name] === 'function') return globalThis[name];
    throw new Error('Could not find function or class ' + name);
  }
  return { call: (name, ...args) => resolve(name)(...args), constructor: name => {
    if (moduleError) throw moduleError;
    if (typeof mod?.[name] === 'function') return mod[name];
    if (typeof mod === 'function') return mod;
    if (typeof mod?.Solution === 'function') return mod.Solution;
    if (typeof globalThis[name] === 'function') return globalThis[name];
    throw new Error('Could not find class ' + name);
  } };
}

function factorial(n) { let value = 1; for (let i = 2; i <= n; i++) value *= i; return value; }
function choose(n, k) { let value = 1; for (let i = 1; i <= k; i++) value = value * (n - i + 1) / i; return value; }
function frequency(sequence, outcomes) {
  const counts = new Map();
  for (const value of sequence) counts.set(value, (counts.get(value) ?? 0) + 1);
  const expected = sequence.length / outcomes;
  const tolerance = Math.max(25, 7 * Math.sqrt(expected * (1 - 1 / outcomes)));
  if (expected >= 50 && counts.size < outcomes) return false;
  return [...counts.values()].every(count => Math.abs(count - expected) <= tolerance);
}
function randomBatch(id, args, call) {
  const samples = 100000;
  const values = id === 'offline_sampling' ? args[1] : ['online_sampling', 'nonuniform_random_number'].includes(id) ? args[0] : [];
  const probabilities = id === 'nonuniform_random_number' ? args[1] : [];
  const n = ['random_permutation', 'random_subset'].includes(id) ? args[0] : values.length;
  const k = id === 'offline_sampling' ? args[0] : ['online_sampling', 'random_subset'].includes(id) ? args[1] : n;
  const lower = args[0], upper = args[1];
  const outcomes = id === 'uniform_random_number' ? upper - lower + 1 : id === 'random_permutation' ? factorial(n) : id === 'nonuniform_random_number' ? values.length : choose(n, k);
  const labels = new Map(), sequence = [];
  for (let i = 0; i < samples; i++) {
    let label;
    if (id === 'uniform_random_number') {
      const x = call('uniformRandom', lower, upper);
      check(Number.isInteger(x) && x >= lower && x <= upper, 'Random value is outside the inclusive bounds.'); label = String(x);
    } else if (id === 'nonuniform_random_number') {
      const x = call('nonuniformRandomNumberGeneration', values.slice(), probabilities.slice()), index = values.indexOf(x);
      check(index >= 0 && probabilities[index] > 0, 'Return one of the positive-probability values.'); label = String(index);
    } else {
      let sample;
      if (id === 'random_permutation') sample = call('computeRandomPermutation', n);
      else if (id === 'random_subset') sample = call('randomSubset', n, k);
      else if (id === 'online_sampling') sample = call('onlineRandomSample', values.slice(), k);
      else {
        const copy = values.slice(); call('randomSampling', k, copy);
        check(same(values, copy), 'Sampling must preserve every original input value.'); sample = copy.slice(0, k);
      }
      check(Array.isArray(sample) && sample.length === (id === 'random_permutation' ? n : k) && new Set(sample).size === sample.length, 'Random sample has the wrong size or duplicate values.');
      check(['random_subset', 'random_permutation'].includes(id) ? sample.every(x => Number.isInteger(x) && x >= 0 && x < n) : sample.every(x => values.includes(x)), 'Random sample contains an invalid value.');
      label = stringify(id === 'random_permutation' ? sample : sample.slice().sort((a, b) => a - b));
    }
    if (!labels.has(label)) labels.set(label, labels.size);
    sequence.push(labels.get(label));
  }
  if (id === 'nonuniform_random_number') {
    const counts = new Map(); for (const value of sequence) counts.set(value, (counts.get(value) ?? 0) + 1);
    return probabilities.every((p, index) => {
      const observed = counts.get(labels.get(String(index))) ?? 0, expected = samples * p;
      return Math.abs(observed - expected) <= Math.max(25, 6 * Math.sqrt(expected * (1 - p)));
    });
  }
  if (!frequency(sequence, outcomes)) return false;
  if (!frequency(sequence.slice(1).map((value, i) => sequence[i] + ',' + value), outcomes * outcomes)) return false;
  return frequency(sequence.slice(2).map((value, i) => sequence[i] + ',' + sequence[i + 1] + ',' + value), outcomes ** 3);
}

function invokeCustom(id, a, call, getConstructor) {
  switch (id) {
    case 'absent_value_array': {
      const original = a[0].slice(), missing = call('findMissingElement', a[0]);
      check(Number.isInteger(missing) && missing >= 0 && !original.includes(missing)); return true;
    }
    case 'alternating_array': case 'even_odd_array': case 'dutch_national_flag': {
      const values = a[0], original = values.slice();
      if (id === 'alternating_array') call('rearrange', values);
      else if (id === 'even_odd_array') call('evenOdd', values);
      else call('dutchFlagPartition', a[1], values);
      check(same(original, values), 'Preserve every input element.');
      if (id === 'alternating_array') {
        for (let i = 1; i < values.length; i++) check(i % 2 ? values[i - 1] <= values[i] : values[i - 1] >= values[i]);
      } else if (id === 'even_odd_array') {
        let odd = false; for (const value of values) { if (value & 1) odd = true; else check(!odd); }
      } else {
        const pivot = original[a[1]]; let previous = -1;
        for (const value of values) { const group = value < pivot ? -1 : value > pivot ? 1 : 0; check(group >= previous); previous = group; }
      }
      return true;
    }
    case 'group_equal_entries': {
      const people = a[0], original = people.map(row => row.slice()); call('groupByAge', people);
      check(same(original, people)); const completed = new Set(); let previous;
      for (const person of people) if (person[0] !== previous) { check(!completed.has(person[0])); completed.add(person[0]); previous = person[0]; }
      return true;
    }
    case 'gray_code': {
      const limit = 2 ** a[0], result = call('grayCode', a[0]);
      check(Array.isArray(result) && result.length === limit && new Set(result).size === limit && result.every(x => Number.isInteger(x) && x >= 0 && x < limit));
      for (let i = 1; i < result.length; i++) { const difference = BigInt(result[i]) ^ BigInt(result[i - 1]); check(difference !== 0n && (difference & (difference - 1n)) === 0n); }
      return true;
    }
    case 'hanoi': {
      const n = a[0], moves = call('computeTowerHanoi', n), pegs = [Array.from({ length: n }, (_, i) => n - i), [], []];
      check(Array.isArray(moves));
      for (const move of moves) {
        check(Array.isArray(move) && move.length === 2 && move.every(x => Number.isInteger(x) && x >= 0 && x < 3) && move[0] !== move[1]);
        const from = pegs[move[0]], to = pegs[move[1]]; check(from.length > 0 && (!to.length || from.at(-1) < to.at(-1))); to.push(from.pop());
      }
      check(pegs[0].length === 0 && (pegs[1].length === n || pegs[2].length === n)); return true;
    }
    case 'is_array_dominated':
      check(call('validPlacementExists', a[0].slice(), a[1].slice()) === a[2]);
      check(call('validPlacementExists', a[1].slice(), a[0].slice()) === a[3]); return true;
    case 'is_string_decomposable_into_words': {
      const dictionary = new Set(a[1]), result = call('decomposeIntoDictionaryWords', a[0], new Set(dictionary));
      check(Array.isArray(result) && (a[2] ? result.join('') === a[0] && result.every(word => dictionary.has(word)) : result.length === 0)); return true;
    }
    case 'search_entry_equal_to_index': {
      const original = a[0].slice(), index = call('searchEntryEqualToItsIndex', a[0]);
      check(Number.isInteger(index) && (index === -1 ? !original.some((value, i) => value === i) : index >= 0 && index < original.length && original[index] === index)); return true;
    }
    case 'refueling_schedule': {
      const gallons = a[0].slice(), distances = a[1].slice(), start = call('findAmpleCity', a[0], a[1]);
      check(Number.isInteger(start) && start >= 0 && start < gallons.length); let tank = 0n;
      for (let i = 0; i < gallons.length; i++) { const city = (start + i) % gallons.length; tank += BigInt(gallons[city]) * 20n - BigInt(distances[city]); check(tank >= 0n); }
      return true;
    }
    case 'run_length_compression':
      check(call('decoding', a[0]) === a[1] && call('encoding', a[1]) === a[0]); return true;
    case 'string_integer_interconversion': {
      const formatted = call('intToString', a[0]), parsed = call('stringToInt', a[1]);
      check(typeof formatted === 'string' && formatted === String(a[0]) && parsed === a[0]); return true;
    }
    case 'pivot_list': {
      const original = listNodes(a[0]).map(node => node.data), result = listNodes(call('listPivoting', a[0], a[1]));
      check(same(original, result.map(node => node.data))); let previous = -1;
      for (const node of result) { const group = node.data < a[1] ? -1 : node.data > a[1] ? 1 : 0; check(group >= previous); previous = group; }
      return true;
    }
    case 'is_list_cyclic': {
      const nodes = listNodes(a[0]), entry = a[1] === -1 ? null : nodes.find(node => node.data === a[1]);
      check(a[1] === -1 || entry != null, 'The cycle entry must exist.');
      if (entry != null) nodes.at(-1).next = entry;
      const snapshot = nodes.map(node => ({ node, data: node.data, next: node.next }));
      check(call('hasCycle', a[0]) === entry, 'Return the actual cycle-entry node, not a copy.'); unchangedList(snapshot); return true;
    }
    case 'do_terminated_lists_overlap': case 'do_lists_overlap': {
      let first = a[0], second = a[1]; const common = a[2];
      const firstNodes = listNodes(first), secondNodes = listNodes(second);
      if (!firstNodes.length) first = common; else firstNodes.at(-1).next = common;
      if (!secondNodes.length) second = common; else secondNodes.at(-1).next = common;
      if (id === 'do_lists_overlap') {
        const n0 = listNodes(first), n1 = listNodes(second);
        if (a[3] >= 0) n0.at(-1).next = n0[a[3]];
        if (a[4] >= 0) n1.at(-1).next = n1[a[4]];
      }
      const n0 = listNodes(first, true), n1 = listNodes(second, true), shared = new Set(n0.filter(node => n1.includes(node)));
      const snapshot = [...new Set([...n0, ...n1])].map(node => ({ node, data: node.data, next: node.next }));
      const result = call('overlappingLists', first, second);
      check(id === 'do_terminated_lists_overlap' ? result === common : shared.size === 0 ? result == null : shared.has(result));
      unchangedList(snapshot); return true;
    }
    case 'copy_posting_list': {
      const input = a[0].map(row => row.slice()), nodes = input.map(row => new PostingListNode(row[0]));
      for (let i = 0; i < nodes.length; i++) { nodes[i].next = nodes[i + 1] ?? null; nodes[i].jump = input[i][1] === -1 ? null : nodes.find(node => node.order === input[i][1]); }
      const original = nodes.map(node => ({ node, order: node.order, next: node.next, jump: node.jump }));
      let copy = call('copyPostingsList', nodes[0] ?? null); const copies = [], seen = new Set();
      while (copy != null) { check(!seen.has(copy) && !nodes.includes(copy)); seen.add(copy); copies.push(copy); copy = copy.next; }
      check(copies.length === nodes.length);
      for (let i = 0; i < copies.length; i++) {
        const jump = input.findIndex(row => row[0] === input[i][1]);
        check(copies[i].order === input[i][0] && copies[i].jump === (input[i][1] === -1 ? null : copies[jump]));
      }
      check(original.every(item => item.node.order === item.order && item.node.next === item.next && item.node.jump === item.jump), 'Preserve the original posting list.'); return true;
    }
    case 'graph_clone': {
      const graph = Array.from({ length: a[0] }, (_, i) => new GraphVertex(i));
      for (const [from, to] of a[1]) graph[from].edges.push(graph[to]);
      const original = graph.map(node => ({ node, label: node.label, edges: node.edges.slice(), labels: node.edges.map(edge => edge.label) }));
      const reachable = new Set(), queue = graph.length ? [graph[0]] : [];
      for (let i = 0; i < queue.length; i++) { const node = queue[i]; if (reachable.has(node.label)) continue; reachable.add(node.label); queue.push(...node.edges); }
      const result = call('cloneGraph', graph[0]); check(result != null && result.label === 0);
      const copies = new Map(), pending = [result];
      for (let i = 0; i < pending.length; i++) {
        const node = pending[i]; check(node != null && Number.isInteger(node.label) && node.label >= 0 && node.label < graph.length && !graph.includes(node));
        if (copies.has(node.label)) { check(copies.get(node.label) === node); continue; }
        copies.set(node.label, node); check(Array.isArray(node.edges) && node.edges.every(edge => edge != null) && same(node.edges.map(edge => edge.label), original[node.label].labels)); pending.push(...node.edges);
      }
      check(copies.size === reachable.size && [...copies.keys()].every(label => reachable.has(label)));
      check(original.every(item => item.node.label === item.label && Array.isArray(item.node.edges) && item.node.edges.length === item.edges.length && item.node.edges.every((edge, i) => edge === item.edges[i])), 'Preserve the original graph.'); return true;
    }
    case 'sorted_list_to_bst': {
      const values = a[0].slice(), nodes = values.map(value => new BinaryTreeNode(value));
      for (let i = 0; i < nodes.length; i++) { nodes[i].left = nodes[i - 1] ?? null; nodes[i].right = nodes[i + 1] ?? null; }
      const result = call('buildBstFromSortedDoublyList', nodes[0] ?? null, values.length);
      check(equal(inorder(result), values)); return true;
    }
    case 'sudoku_solve': {
      const original = a[0].map(row => row.slice()), board = a[0], n = board.length, width = Math.sqrt(n); call('solveSudoku', board);
      check(Array.isArray(board) && board.length === n && board.every(row => Array.isArray(row) && row.length === n));
      for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) check(Number.isInteger(board[r][c]) && board[r][c] >= 1 && board[r][c] <= n && (!original[r][c] || original[r][c] === board[r][c]));
      for (let i = 0; i < n; i++) {
        check(new Set(board[i]).size === n && new Set(board.map(row => row[i])).size === n); const block = [];
        for (let r = 0; r < width; r++) for (let c = 0; c < width; c++) block.push(board[Math.floor(i / width) * width + r][i % width * width + c]);
        check(new Set(block).size === n);
      }
      return true;
    }
    case 'adding_credits': {
      const Type = getConstructor('AddingCredits'); let store = new Type();
      // Keep an independent oracle, including when submitted Lookup is incorrect.
      const expectedCredits = new Map();
      for (const [op, text, value] of a[0]) {
        if (op === 'ClientsCreditsInfo') { store = new Type(); expectedCredits.clear(); }
        else if (op === 'insert') { store.insert(text, value); expectedCredits.set(text, BigInt(value)); }
        else if (op === 'remove') { check(store.remove(text) === (value === 1)); expectedCredits.delete(text); }
        else if (op === 'lookup') check(store.lookup(text) === value);
        else if (op === 'add_all') {
          store.addAll(value);
          for (const [client, credit] of expectedCredits) expectedCredits.set(client, credit + BigInt(value));
        } else if (op === 'max') {
          const actual = store.max();
          check(expectedCredits.size === 0 ? actual === ''
            : expectedCredits.has(actual) && [...expectedCredits.values()].every(credit => credit <= expectedCredits.get(actual)));
        } else throw new Error('Unknown credits operation: ' + op);
      }
      return true;
    }
    case 'lru_cache': {
      const Type = getConstructor('LruCache'); let store;
      for (const [op, key, value] of a[0]) {
        if (op === 'LruCache') store = new Type(key);
        else if (op === 'lookup') check(store.lookup(key) === value);
        else if (op === 'insert') store.insert(key, value);
        else if (op === 'erase') check(store.erase(key) === (value === 1));
        else throw new Error('Unknown cache operation: ' + op);
      }
      return true;
    }
    case 'circular_queue': case 'queue_from_stacks': case 'queue_with_max': case 'stack_with_max': {
      const name = { circular_queue: 'CircularQueue', queue_from_stacks: 'QueueFromStacks', queue_with_max: 'QueueWithMax', stack_with_max: 'StackWithMax' }[id];
      const Type = getConstructor(name); let store = id === 'circular_queue' ? new Type(1) : new Type();
      for (const [op, value] of a[0]) {
        if (['Queue', 'Stack', 'QueueWithMax'].includes(op)) store = id === 'circular_queue' ? new Type(value) : new Type();
        else if (op === 'enqueue') store.enqueue(value);
        else if (op === 'dequeue') check(store.dequeue() === value);
        else if (op === 'size') check(store.size() === value);
        else if (op === 'push') store.push(value);
        else if (op === 'pop') check(store.pop() === value);
        else if (op === 'max') check(store.max() === value);
        else if (op === 'empty') check(store.empty() === (value === 1));
        else throw new Error('Unknown container operation: ' + op);
      }
      return true;
    }
    case 'nonuniform_random_number': case 'uniform_random_number': case 'random_permutation': case 'random_subset': case 'offline_sampling': case 'online_sampling':
      for (let attempt = 0; attempt < 3; attempt++) if (randomBatch(id, a, call)) return true;
      throw new JudgeValidationException('The generated samples failed distribution or independence checks.');
    case 'bst_from_sorted_array': {
      const original = a[0].slice(), tree = call('buildMinHeightBstFromSortedArray', a[0]); check(equal(inorder(tree), original));
      const heights = new Map(), nodes = treeNodes(tree);
      for (let i = nodes.length - 1; i >= 0; i--) heights.set(nodes[i], 1 + Math.max(heights.get(nodes[i].left) ?? 0, heights.get(nodes[i].right) ?? 0));
      return tree == null ? 0 : heights.get(tree);
    }
    case 'bst_to_sorted_list': {
      const originalNodes = treeNodes(a[0]), expected = inorder(a[0]), originalValues = new Map(originalNodes.map(node => [node, node.data]));
      let node = call('bstToDoublyLinkedList', a[0]), previous = null; const seen = new Set(), output = [];
      while (node != null) {
        check(!seen.has(node) && node.left === previous && originalValues.has(node) && node.data === originalValues.get(node));
        seen.add(node); output.push(node.data); previous = node; node = node.right;
      }
      check(equal(output, expected) && seen.size === originalNodes.length, 'Reuse every original tree node in the doubly linked list.'); return output;
    }
    case 'tree_right_sibling': {
      const snapshot = snapshotTree(a[0]), queue = a[0] == null ? [] : [a[0]], levels = [];
      for (let start = 0; start < queue.length;) {
        const end = queue.length, level = queue.slice(start, end); levels.push(level);
        while (start < end) { const node = queue[start++]; if (node.left != null) queue.push(node.left); if (node.right != null) queue.push(node.right); }
      }
      call('constructRightSibling', a[0]); unchangedTree(snapshot);
      for (const level of levels) for (let i = 0; i < level.length; i++) check(level[i].next === (level[i + 1] ?? null));
      return levels.map(level => level.map(node => node.data));
    }
    case 'search_maze': {
      const original = a[0].map(row => row.slice()), start = a[1].slice(), end = a[2].slice(), path = call('searchMaze', a[0], a[1], a[2]);
      check(Array.isArray(path)); if (!path.length) return equal(start, end);
      check(equal(path[0], start) && equal(path.at(-1), end));
      for (let i = 0; i < path.length; i++) {
        const cell = path[i]; check(Array.isArray(cell) && cell.length === 2); const [r, c] = cell;
        check(Number.isInteger(r) && Number.isInteger(c) && r >= 0 && r < original.length && c >= 0 && c < original[r].length && original[r][c] === 0);
        if (i) check(Math.abs(r - path[i - 1][0]) + Math.abs(c - path[i - 1][1]) === 1);
      }
      return true;
    }
    case 'smallest_subarray_covering_set': case 'smallest_subarray_covering_all_values': {
      const paragraph = a[0].slice(), keywords = Array.from(a[1]);
      const range = id === 'smallest_subarray_covering_set' ? call('findSmallestSubarrayCoveringSet', a[0], new Set(keywords)) : call('findSmallestSequentiallyCoveringSubset', a[0], keywords.slice());
      check(Array.isArray(range) && range.length === 2 && range.every(Number.isInteger) && range[0] >= 0 && range[1] >= range[0] && range[1] < paragraph.length);
      const slice = paragraph.slice(range[0], range[1] + 1);
      if (id === 'smallest_subarray_covering_set') check(keywords.every(word => slice.includes(word)));
      else { let k = 0; for (const word of slice) if (k < keywords.length && word === keywords[k]) k++; check(k === keywords.length); }
      return range[1] - range[0] + 1;
    }
    default: return undefined;
  }
}

const customIds = new Set([
  'absent_value_array', 'alternating_array', 'even_odd_array', 'dutch_national_flag',
  'group_equal_entries', 'gray_code', 'hanoi', 'is_array_dominated',
  'is_string_decomposable_into_words', 'search_entry_equal_to_index', 'refueling_schedule',
  'run_length_compression', 'string_integer_interconversion', 'pivot_list', 'is_list_cyclic',
  'do_terminated_lists_overlap', 'do_lists_overlap', 'copy_posting_list', 'graph_clone',
  'sorted_list_to_bst', 'sudoku_solve', 'adding_credits', 'lru_cache', 'circular_queue',
  'queue_from_stacks', 'queue_with_max', 'stack_with_max', 'nonuniform_random_number',
  'uniform_random_number', 'random_permutation', 'random_subset', 'offline_sampling',
  'online_sampling', 'bst_from_sorted_array', 'bst_to_sorted_list', 'tree_right_sibling',
  'search_maze', 'smallest_subarray_covering_set', 'smallest_subarray_covering_all_values'
]);

const tests = losslessParse(fs.readFileSync(0, 'utf8')), results = [];
for (const test of tests) {
  const started = performance.now(); let actual = null, error = null, validationFailed = false, validationMessage = null;
  try {
    const a = test.map((value, i) => convert(value, argumentTypes[i] ?? '')), ctx = context();
    if (customIds.has(problemId)) actual = invokeCustom(problemId, a, ctx.call, ctx.constructor);
    else {
      const stable = problemId === 'sort_list' ? snapshotList(a[0]) : null;
      const output = ctx.call(targetName, ...a);
      if (stable != null) {
        const nodes = listNodes(output), byValue = new Map();
        for (const item of stable) { if (!byValue.has(item.data)) byValue.set(item.data, []); byValue.get(item.data).push(item.node); }
        const originals = new Set(stable.map(item => item.node));
        check(nodes.length === stable.length && nodes.every(node => originals.has(node)), 'Stable sort must reuse every original node.');
        const originalValues = new Map(stable.map(item => [item.node, item.data]));
        for (const node of nodes) check(originalValues.get(node) === node.data && byValue.get(node.data)?.shift() === node, 'Preserve the relative identity of equal-valued nodes.');
      }
      actual = serialize(output, resultType);
    }
  } catch (exception) {
    if (exception instanceof JudgeValidationException) { validationFailed = true; validationMessage = String(exception.message ?? '').slice(0, 2000); }
    else error = String((exception.name ?? 'Error') + ': ' + (exception.message ?? exception)).slice(0, 2000);
  }
  results.push({ actual, error, validationFailed, validationMessage, elapsedMs: performance.now() - started });
}
writeOutput(stringify(results));
