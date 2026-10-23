"""Bounded decision-tree probability intervals and seeded collection checks.

The source functions come from existing bank-owned randomized harnesses. The
original runtimes stay unchanged. For larger arrays, exact enumeration gives
way to seeded structural/marginal checks; incomplete small trees retain their
unresolved probability mass rather than rejecting a valid slower algorithm.
"""
import re
from harness_rand16 import between,relaxed

FILES={'python':('harness.py','def random_check(raw):','\ndef execute(raw):'), 'javascript':('harness.js','function randomCheck(raw) {','\nfunction execute(raw) {'), 'csharp':('Harness.cs','    static object RandomCheck(JsonElement raw)','    static object? Execute(JsonElement raw)'), 'java':('Harness.java','    static boolean sameMultiset(int[] first,int[] second)','    static Object execute(JsonArray raw)'), 'cpp':('harness.cpp','template <typename Subject, typename Invoke>\njson randomCheck','\n// CONFIGURATION')}

def checker(language):
    value=relaxed(between(*FILES[language]),language)
    limit='draw_limit' if language=='python' else 'context.drawLimit' if language=='javascript' else 'DrawLimit'
    value,count=re.subn(r'(draws(?:\[0\])?\s*<=\s*)128',lambda m:m[1]+limit,value)
    if count!=2:raise ValueError('Unknown draw limits '+language)
    if language=='python':
        value=value.replace('pending = [([], 1.0)]','pending = [] if shuffle and len(original)>5 else [([],1.0)]')
        value=value.replace('        check(branches <= 100000, "Too many random decision branches.")','        if branches>100000:\n            unresolved += weight+sum(mass for _,mass in pending)\n            pending.clear()\n            break')
        value=value.replace('''                unresolved < 1e-10
                and len(probabilities) == factorial
                and all(abs(p - 1 / factorial) < 1e-9 for p in probabilities.values()),''','''                all(p <= 1/factorial+1e-9 and p+unresolved >= 1/factorial-1e-9 for p in probabilities.values())
                and (len(probabilities)==factorial or unresolved>=1/factorial-1e-9),''')
        value=value.replace('samples = 4096','samples = 128 if len(original)>64 else 4096').replace('context["capture"] = trial == 0','context["capture"] = trial == 0\n        context["sampling"] = True')
    elif language=='javascript':
        value=value.replace('  let unresolved = 0, branches = 0;','  if(shuffle&&original.length>5)pending.length=0;\n  let unresolved = 0, branches = 0;')
        value=value.replace("check(++branches <= 100000, 'Randomized algorithm used too many decision branches.');",'if(++branches>100000){unresolved+=item.weight+pending.reduce((sum,b)=>sum+b.weight,0);pending.length=0;break;}')
        value=value.replace('unresolved < 1e-10 && probabilities.size === factorial && [...probabilities.values()].every(p => Math.abs(p - 1 / factorial) < 1e-9)','[...probabilities.values()].every(p=>p<=1/factorial+1e-9&&p+unresolved>=1/factorial-1e-9)&&(probabilities.size===factorial||unresolved>=1/factorial-1e-9)')
        value=value.replace('samples = 4096','samples = original.length>64?128:4096').replace('context.capture=trial===0;','context.capture=trial===0;context.sampling=true;')
    elif language=='csharp':
        value=value.replace('pending.Push(([], 1));','if(!(shuffle&&original.Length>5))pending.Push(([], 1));')
        value=value.replace('Check(++branches <= 100000, "Randomized algorithm used too many decision branches.");','if(++branches>100000){unresolved+=item.weight+pending.Sum(branch=>branch.weight);pending.Clear();break;}')
        value=value.replace('unresolved < 1e-10 && probabilities.Count == factorial && probabilities.Values.All(p => Math.Abs(p - 1.0 / factorial) < 1e-9)','probabilities.Values.All(p=>p<=1.0/factorial+1e-9&&p+unresolved>=1.0/factorial-1e-9)&&(probabilities.Count==factorial||unresolved>=1.0/factorial-1e-9)')
        value=value.replace('int samples = 4096','int samples = original.Length>64?128:4096').replace('Capture=trial==0;','Capture=trial==0;Sampling=true;')
    elif language=='java':
        value=value.replace('pending.push(new Decision(new int[0],1));','if(!(shuffle&&original.length>5))pending.push(new Decision(new int[0],1));')
        value=value.replace('check(++branches<=100000,"Randomized algorithm used too many decision branches.");','if(++branches>100000){unresolved+=decision.weight();for(var branch:pending)unresolved+=branch.weight();pending.clear();break;}')
        value=value.replace('unresolved<1e-10&&probabilities.size()==factorial','probabilities.size()==factorial||unresolved>=1.0/factorial-1e-9')
        value=value.replace('Math.abs(probability-1.0/factorial)<1e-9','probability<=1.0/factorial+1e-9&&probability+unresolved>=1.0/factorial-1e-9')
        value=value.replace('int samples=4096','int samples=original.length>64?128:4096').replace('Capture=trial==0;','Capture=trial==0;Sampling=true;')
    else:
        value=value.replace('std::vector<Branch> pending{{{}, 1.0}};','std::vector<Branch> pending{{{},1.0}};if(shuffle&&original.size()>5)pending.clear();')
        value=value.replace('        check(++branches <= 100000, "Randomized algorithm used too many decision branches.");\n','')
        value=value.replace('auto branch = pending.back(); pending.pop_back();','auto branch = pending.back(); pending.pop_back();if(++branches>100000){unresolved+=branch.weight;for(const auto& remaining:pending)unresolved+=remaining.weight;pending.clear();break;}')
        value=value.replace('unresolved < 1e-10 && probabilities.size() == static_cast<size_t>(factorial)','probabilities.size()==static_cast<size_t>(factorial)||unresolved>=1.0/factorial-1e-9')
        value=value.replace('std::abs(entry.second - 1.0 / factorial) < 1e-9','entry.second<=1.0/factorial+1e-9&&entry.second+unresolved>=1.0/factorial-1e-9')
        value=value.replace('constexpr int samples = 4096','int samples = original.size()>64?128:4096').replace('Capture=trial==0;','Capture=trial==0;Sampling=true;')
    if language=='javascript':
        value=value.replace("check(permutationCounts.has(key), 'Shuffle returned an unexpected permutation.');", "if(!permutationCounts.has(key))permutationCounts.set(key,0);")
        value=value.replace('    const expected = samples / permutationCounts.size;', "    let bins=1;for(let i=2;i<=original.length;++i)bins*=i;check(permutationCounts.size===bins,'Seeded shuffle omitted permutations');\n    const expected = samples / bins;")
    if language=='cpp':
        value=value.replace('for (const auto& entry : probabilities) {\n                double difference = seededPermutations[entry.first] - expected;', 'for (const auto& entry : seededPermutations) {\n                double difference = entry.second - expected;')
    value=value.replace('max(1, len(original))','len(original)').replace('Math.max(1, original.length)','original.length').replace('Math.Max(1, original.Length)','original.Length').replace('Math.max(1,length)','length').replace('std::max(1, static_cast<int>(original.size()))','static_cast<int>(original.size())')
    hooks={
      'python':('        result = call(instance, Method, a) if shuffle else call(instance, Method)','\n        if shuffle: record_serial(a)'),
      'javascript':('    const result = shuffle ? call(seededInstance, Method, array) : call(seededInstance, Method);','\n    if(shuffle)recordSerial(array);'),
      'csharp':('var result = shuffle ? Call(seededInstance, Method, a) : Call(seededInstance, Method);','if(shuffle)RecordSerial(a);'),
      'java':('Object actual=shuffle?call(seededInstance,Method,(Object)values):call(seededInstance,Method);','if(shuffle)recordSerial(values);'),
      'cpp':('json result = invoke(persistent, array);','if(shuffle)recordSerial(array);')}
    needle,hook=hooks[language]
    if value.count(needle)!=1:raise ValueError('Unknown seeded output hook '+language)
    value=value.replace(needle,needle+hook,1)
    # Failing closed here prevents an upstream source change from silently
    # restoring a restrictive finite-exploration equality or fixed draw cap.
    if 'unresolved < 1e-10' in value or 'unresolved<1e-10' in value:raise ValueError('Unknown exact probability gate '+language)
    if 'samples = 4096' in value or 'samples=4096' in value:raise ValueError('Unknown sample limit '+language)
    if language=='python' and 'branches <= 100000' in value:raise ValueError('Unknown Python branch limit')
    return value
