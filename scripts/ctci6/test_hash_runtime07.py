"""Batch both generic instantiations into each compiled mutation/alternative."""
import json
import unittest
from algorithms_hash07 import body
from chapter07 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_hash07 import make,oracle,valid_observation
from models07 import declare
from verify01 import execute

def replace_member(code,language,name,replacement):
    if language=='python':
        start=code.index('\n    def '+name+'(');end=code.find('\n    def ',start+1)
        if end<0:end=len(code)
        signature=code[start:code.index('\n',start+1)]
        return code[:start]+signature+'\n'+'\n'.join('        '+line for line in replacement.splitlines())+'\n'+code[end:]
    start=code.index(name+'(');opening=code.index('{',start);depth=1;end=opening+1
    while depth:depth+=(code[end]=='{')-(code[end]=='}');end+=1
    return code[:opening+1]+replacement+code[end-1:]

class HashRuntimeTests(unittest.TestCase):
    def run_code(self,language,label,code):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='7.12');config=entry['languages'][language];spec=next(s for s in SPECS if s['ref']=='7.12');_,code=declare(spec,language,code)
        filename='HashTable.java' if language=='java' else ('Solution.' if language=='csharp' else 'solution.')+EXT[language]
        cases=[]
        for kind,keys,values,updated in [('text-number',['alpha','beta','gamma'],[0,9,-2147483648],7),('number-text',[32768,65536,-2147483648],['','nine','🌲'],'replacement')]:
            default=0 if kind=='text-number' else ''
            actions=[('Put',k,v) for k,v in zip(keys,values)]+[('Put',keys[0],updated),('Get',keys[0],default),('Get',keys[1],default),('Remove',keys[1],default),('Get',keys[1],default),('Contains',keys[2],default),('Remove',keys[0],default),('Get',keys[2],default),('Remove',keys[2],default),('Contains',keys[0],default),('Remove',keys[0],default)]
            args=make(kind,1,actions);cases.append(dict(ref='7.12',arguments=args,expected=oracle('7.12',args)))
        rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-hash7-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
        return cases,[r['observation'] for r in rows]
    def test_wrong_key_matches_duplicate_entries_and_noop_remove_fail(self):
        for language in LANGUAGES:
            original=body(language)
            if language=='python':
                identity=original.replace('node.key==key','node.key is key')
                duplicate=replace_member(original,language,'Put','slot=self._index(key)\nself._buckets[slot]=HashTable._Node(key,value,self._buckets[slot])')
                noop=replace_member(original,language,'Remove','return self.Contains(key)')
            elif language=='javascript':
                identity=original.replace('if(node.key===key)','if(true)')
                duplicate=replace_member(original,language,'Put','const slot=this.index(key);this.buckets[slot]={key,value,next:this.buckets[slot]};')
                noop=replace_member(original,language,'Remove','return this.Contains(key);')
            elif language=='csharp':
                identity=original.replace('EqualityComparer<K>.Default.Equals(node.Key,key)','object.ReferenceEquals(node.Key,key)')
                duplicate=replace_member(original,language,'Put','int index=Index(key);buckets[index]=new Node(key,value,buckets[index]);')
                noop=replace_member(original,language,'Remove','return Contains(key);')
            elif language=='java':
                identity=original.replace('Objects.equals(node.key,key)','node.key==key')
                duplicate=replace_member(original,language,'Put','int slot=index(key);buckets.set(slot,new Node<>(key,value,buckets.get(slot)));')
                noop=replace_member(original,language,'Remove','return Contains(key);')
            else:
                identity=original.replace('std::equal_to<K>{}(node->key,key)','&node->key==&key')
                duplicate=replace_member(original,language,'Put','auto slot=index(key);buckets[slot]=new Node(key,value,buckets[slot]);')
                noop=replace_member(original,language,'Remove','return Contains(key);')
            for label,code in [('wrong-key-match',identity),('duplicate-entries',duplicate),('noop-remove',noop)]:
                with self.subTest(language=language,variant=label):
                    self.assertNotEqual(original,code);cases,observed=self.run_code(language,label,code)
                    for case,value in zip(cases,observed):self.assertFalse(valid_observation('7.12',case,value))
    def test_tail_insertion_preserves_the_map_contract(self):
        tails={
'python':'node=self._find(key)\nif node is not None:\n    node.value=value\n    return\nslot=self._index(key)\nadded=HashTable._Node(key,value,None)\nif self._buckets[slot] is None:\n    self._buckets[slot]=added\n    return\ntail=self._buckets[slot]\nwhile tail.next is not None:\n    tail=tail.next\ntail.next=added',
'javascript':'const old=this.find(key);if(old!==null){old.value=value;return;}const slot=this.index(key),added={key,value,next:null};if(this.buckets[slot]===null){this.buckets[slot]=added;return;}let tail=this.buckets[slot];while(tail.next!==null)tail=tail.next;tail.next=added;',
'csharp':'var old=Find(key);if(old is not null){old.Value=value;return;}int slot=Index(key);var added=new Node(key,value,null);if(buckets[slot] is null){buckets[slot]=added;return;}var tail=buckets[slot]!;while(tail.Next is not null)tail=tail.Next;tail.Next=added;',
'java':'var old=find(key);if(old!=null){old.value=value;return;}int slot=index(key);var added=new Node<K,V>(key,value,null);if(buckets.get(slot)==null){buckets.set(slot,added);return;}var tail=buckets.get(slot);while(tail.next!=null)tail=tail.next;tail.next=added;',
'cpp':'if(Node* old=find(key)){old->value=value;return;}auto slot=index(key);Node* added=new Node(key,value,nullptr);if(!buckets[slot]){buckets[slot]=added;return;}Node* tail=buckets[slot];while(tail->next)tail=tail->next;tail->next=added;'}
        for language in LANGUAGES:
            with self.subTest(language=language):
                code=replace_member(body(language),language,'Put',tails[language]);cases,observed=self.run_code(language,'tail-insertion',code)
                for case,value in zip(cases,observed):self.assertNotIn('error',value);self.assertTrue(valid_observation('7.12',case,value))
if __name__=='__main__':unittest.main()
