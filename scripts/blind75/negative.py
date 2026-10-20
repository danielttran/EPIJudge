"""Nonconstant adversaries: correct values with broken identity/mutation, or altered results."""
from generate import TYPES, STATE

CLONE={
'csharp':'public static ListNode? CloneList(ListNode? n){return Link(Nodes(n).Select(x=>new ListNode(x.val)));}',
'java':'static ListNode cloneList(ListNode n){List<ListNode>a=new ArrayList<>();for(ListNode x:nodes(n))a.add(new ListNode(x.val));return link(a);}',
'cpp':'ListNode* cloneList(ListNode*n){auto a=nodes(n);for(auto&x:a)x=new ListNode(x->val);return link(a);}',
'javascript':'cloneList(n){return this.link(this.nodes(n).map(x=>new ListNode(x.val)));},',
'python':'    @staticmethod\n    def clone_list(n): return Probe.link([ListNode(x.val) for x in Probe.nodes(n)])\n'}

def make(s,lang,correct_bodies,extra):
    mode=s['mode'];m=s['method'];py=lang=='python';cpp=lang=='cpp';js=lang=='javascript';cs=lang=='csharp';java=lang=='java'
    sep='::' if cpp else '.';probe='Probe'+sep;args=', '.join(p['name'] for p in s['params']);fn='ActualCorrect' if lang in ('csharp','cpp') else 'actual_correct' if py else 'actualCorrect'
    call=fn+'('+args+')';result=s['result'];semi='' if py else ';'
    def select(cs_,js_,py_,cpp_,java_):return dict(csharp=cs_,javascript=js_,python=py_,cpp=cpp_,java=java_)[lang]
    def output(expr):return 'return '+expr+semi
    if mode in STATE:
        bodies=dict(correct_bodies);fields=''
        if mode=='strings_codec':
            bodies['Encode']=select('return string.Join("|",strings);','return strings.join("|");','return "|".join(strings)','std::string out;for(size_t i=0;i<strings.size();i++){if(i)out+="|";out+=strings[i];}return out;','return String.join("|",strings);')
            bodies['Decode']=select('return encoded.Split(\'|\');','return encoded.split("|");','return encoded.split("|")','std::vector<std::string>out;size_t i=0;while(true){auto j=encoded.find(\'|\',i);out.push_back(encoded.substr(i,j==std::string::npos?j:j-i));if(j==std::string::npos)break;i=j+1;}return out;','return encoded.split(java.util.regex.Pattern.quote("|"),-1);')
        elif mode=='tree_codec':
            fields=select('private static TreeNode? original;','static original=null;','    original=None\n','inline static TreeNode* original=nullptr;','private static TreeNode original;')
            owner='Codec.' if js or py else ''
            bodies['Serialize']=owner+'original=root'+semi+'\n'+correct_bodies['Serialize']
            bodies['Deserialize']=output(owner+'original')
        elif mode=='trie':bodies['Search']=select('return words.Any(w=>w.StartsWith(word,StringComparison.Ordinal));','return [...this.words].some(w=>w.startsWith(word));','return any(w.startswith(word) for w in self.words)','return std::any_of(words.begin(),words.end(),[&](const auto&w){return w.compare(0,word.size(),word)==0;});','return words.stream().anyMatch(w->w.startsWith(word));')
        elif mode=='dictionary':bodies['Search']=select('return words.Any(w=>w.Length>=pattern.Length&&pattern.Select((c,i)=>c==\'.\'||c==w[i]).All(v=>v));','return [...this.words].some(w=>w.length>=pattern.length&&[...pattern].every((c,i)=>c==="."||c===w[i]));','return any(len(w)>=len(pattern) and all(p=="." or p==c for p,c in zip(pattern,w)) for w in self.words)','for(auto&w:words){if(w.size()<pattern.size())continue;bool ok=true;for(size_t i=0;i<pattern.size();i++)ok&=pattern[i]==\'.\'||pattern[i]==w[i];if(ok)return true;}return false;','for(String w:words){if(w.length()<pattern.length())continue;boolean ok=true;for(int i=0;i<pattern.length();i++)ok&=pattern.charAt(i)==\'.\'||pattern.charAt(i)==w.charAt(i);if(ok)return true;}return false;')
        elif mode=='median':bodies['FindMedian']=select('return values[(values.Count-1)/2];','return this.values[Math.floor((this.values.length-1)/2)];','return self.values[(len(self.values)-1)//2]','return values[(values.size()-1)/2];','return values.get((values.size()-1)/2);')
        return bodies,extra,fields,None
    first=select('var value='+call+';','let value='+call+';','value='+call,'auto value='+call+';',TYPES['java'][result]+' value='+call+';') if result!='void' else call+semi
    if mode in ('list_reuse','list_remove'):
        expression=probe+('CloneList' if cs else 'clone_list' if py else 'cloneList')+'(value)'
        broken=first+'\n'+output(expression)
        # The list cloning helper is inserted into the shared fixture helper.
        if cs or java:extra=extra.replace('class Probe {','class Probe {\n'+CLONE[lang])
        elif cpp:extra=extra.replace('namespace Probe {','namespace Probe {\nListNode* cloneList(ListNode*);')+'\nnamespace Probe{'+CLONE[lang]+'}\n'
        elif js:extra=extra.replace('const Probe={','const Probe={\n'+CLONE[lang])
        else:extra=extra.replace('class Probe:\n','class Probe:\n'+CLONE[lang])
    elif mode=='list_reorder':
        clone=select('if(head?.next!=null)head.next=Probe.CloneList(head.next);','if(head&&head.next)head.next=Probe.cloneList(head.next);','if head and head.next:head.next=Probe.clone_list(head.next)','if(head&&head->next)head->next=Probe::cloneList(head->next);','if(head!=null&&head.next!=null)head.next=Probe.cloneList(head.next);')
        # Reuse the list helper insertion from a synthetic list-reuse mode.
        fake=dict(s,mode='list_reuse',result='list');_,extra,_,_=make(fake,lang,correct_bodies,extra)
        broken=first+'\n'+clone
    elif mode=='matrix_inplace':broken=first+'\n'+select('for(int i=0;i<matrix.Length;i++)matrix[i]=matrix[i].ToArray();','for(let i=0;i<matrix.length;i++)matrix[i]=[...matrix[i]];','for i in range(len(matrix)):matrix[i]=list(matrix[i])','auto replacement=matrix;matrix.swap(replacement);','for(int i=0;i<matrix.length;i++)matrix[i]=matrix[i].clone();')
    elif mode=='list_cycle':broken=first+'\n'+select('if(head!=null)head.val^=1;','if(head)head.val^=1;','if head:head.val^=1','if(head)head->val^=1;','if(head!=null)head.val^=1;')+'\n'+output('value')
    elif mode=='tree_inplace':broken=first+'\n'+output(probe+('Deserialize' if cs else 'deserialize')+'('+probe+('Serialize' if cs else 'serialize')+'(value))')
    elif mode=='tree_node':broken=first+'\n'+output(select('value==null?null:new TreeNode(value.val)','value?new TreeNode(value.val):null','TreeNode(value.val) if value else None','value?new TreeNode(value->val):nullptr','value==null?null:new TreeNode(value.val)'))
    elif mode=='graph_clone':broken=output('node')
    elif result in ('i','l'):broken=first+'\n'+output('value ^ 1')
    elif result=='b':broken=first+'\n'+output('not value' if py else '!value')
    elif result=='s':broken=first+'\n'+output('value + "!"')
    elif result=='tree':broken=first+'\n'+select('if(value!=null)value.val^=1;','if(value)value.val^=1;','if value:value.val^=1','if(value)value->val^=1;','if(value!=null)value.val^=1;')+'\n'+output('value')
    else:broken=first+'\n'+select('return value.Length==0?value:value.Concat(value.Take(1)).ToArray();','return value.length?[...value,value[0]]:value;','return value+[value[0]] if value else value','if(!value.empty())value.push_back(value.front());return value;','if(value.length==0)return value;var outp=Arrays.copyOf(value,value.length+1);outp[value.length]=value[0];return outp;')
    # Build a second ordinary method with real parameter binding; it never closes over mutable parameters.
    paramlist=', '.join(TYPES[lang][p['type']]+((' &' if p['type'].startswith('a') else ' ') if cpp else ' ')+p['name'] for p in s['params']) if not (py or js) else ', '.join(p['name'] for p in s['params'])
    implementation=correct_bodies[m]
    if py:helper='def '+fn+'('+paramlist+'):\n'+'\n'.join('    '+line for line in implementation.splitlines())+'\n'
    elif js:helper='function '+fn+'('+paramlist+'){\n'+implementation+'\n}\n'
    else:helper=('public ' if cs or java else '')+TYPES[lang][result]+' '+fn+'('+paramlist+'){\n'+implementation+'\n}\n'
    return {m:broken},extra,'',helper
