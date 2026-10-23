"""Compile caller-alias, invalid-index and shared-iterator mutants, plus inverse offsets."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from models07 import declare
from algorithms07 import body
from chapter07 import SPECS
from corpus07 import make,oracle,valid_observation

class CircularRuntimeTests(unittest.TestCase):
    def run_code(self,language,label,code,kind,initial,actions):
        from verify01 import execute
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='7.9');config=entry['languages'][language]
        _,code=declare(SPECS[0],language,code)
        filename='CircularArray.java' if language=='java' else ('Solution.' if language=='csharp' else 'solution.')+EXT[language]
        args=make(kind,initial,actions);case=dict(ref='7.9',arguments=args,expected=oracle('7.9',args))
        rows=execute(language,False,[case],ROOT/'.epi-runs/ctci6-circular7-variants'/language/(label+'-'+kind),source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
        return case,rows[0]['observation']
    def test_aliasing_negative_indices_and_shared_cursors_are_rejected(self):
        for language in LANGUAGES:
            original=body('7.9',language)
            if language=='python':
                alias=original.replace('initialValues.copy()','initialValues')
                badindex=original.replace('index<0 or ','')
                shared=original.replace('for index in range(len(self._items)):\n            yield','self._cursor=0\n        while self._cursor<len(self._items):\n            index=self._cursor\n            self._cursor+=1\n            yield')
            elif language=='javascript':
                alias=original.replace('initialValues.slice()','initialValues')
                badindex=original.replace('index<0||','')
                shared=original.replace('*[Symbol.iterator](){for(let index=0;index<this.items.length;++index)yield this.items[(this.head+index)%this.items.length];}', '*[Symbol.iterator](){this.cursor=0;while(this.cursor<this.items.length){const index=this.cursor++;yield this.items[(this.head+index)%this.items.length];}}')
            elif language=='csharp':
                alias=original.replace('items=initialValues.ToArray()','items=initialValues')
                badindex=original.replace('index<0||','')
                shared=original.replace('private int head;','private int head;private int sharedCursor;').replace('for(int index=0;index<items.Length;++index)yield return items[(head+index)%items.Length];','sharedCursor=0;while(sharedCursor<items.Length){int index=sharedCursor++;yield return items[(head+index)%items.Length];}')
            elif language=='java':
                alias=original.replace('private final ArrayList<T> items;','private final List<T> items;').replace('items=new ArrayList<>(initialValues)','items=initialValues')
                badindex=original.replace('index<0||','')
                shared=original.replace('private int head;','private int head;private int sharedCursor;').replace('public Iterator<T> iterator(){return','public Iterator<T> iterator(){sharedCursor=0;return').replace('private int cursor;','').replace('cursor','sharedCursor')
            else:
                alias=original.replace('std::vector<T> items;','std::vector<T>& items;').replace('items(initialValues)','items(const_cast<std::vector<T>&>(initialValues))')
                badindex=original.replace('index<0||','')
                shared=original.replace('int head=0;','int head=0;mutable std::size_t sharedCursor=0;').replace('owner->head+cursor','owner->head+owner->sharedCursor').replace('++cursor;return *this;','cursor=++owner->sharedCursor;return *this;').replace('begin()const{return','begin()const{sharedCursor=0;return')
            self.assertNotEqual(original,alias);self.assertNotEqual(original,badindex);self.assertNotEqual(original,shared)
            for kind,initial,replacement in [('number',[3,4,5],9),('text',['fir','oak','elm'],'ash')]:
                default=0 if kind=='number' else ''
                for label,code,actions in [('alias',alias,[('Set',0,replacement),('Iterate',0,default)]),('negative-index',badindex,[('Rotate',1,default),('Get',-1,default)]),('shared-cursor',shared,[('IterateTwice',0,default)])]:
                    with self.subTest(language=language,kind=kind,variant=label):
                        case,observed=self.run_code(language,label,code,kind,initial,actions)
                        self.assertFalse(valid_observation('7.9',case,observed));self.assertIn('error',observed)
    def test_inverse_offset_representation_is_valid(self):
        for language in LANGUAGES:
            original=body('7.9',language)
            if language=='python':code=original.replace('self._head+index','index-self._head').replace('self._head+shift','self._head-shift')
            elif language=='javascript':code=original.replace('this.head+index','index-this.head+this.items.length').replace('this.head+step','this.head-step+size')
            elif language=='csharp':code=original.replace('head+index','index-head+items.Length').replace('head+step','head-step+items.Length')
            elif language=='java':code=original.replace('head+index','index-head+items.size()').replace('head+Math.floorMod(shift,items.size())','head-Math.floorMod(shift,items.size())+items.size()')
            else:code=original.replace('head+index','index-head+static_cast<int>(items.size())').replace('owner->head+cursor','cursor+owner->items.size()-owner->head').replace('head+step','head-step+size')
            self.assertNotEqual(original,code)
            for kind,initial,replacement in [('number',[3,4,5],9),('text',['fir','oak','elm'],'ash')]:
                default=0 if kind=='number' else ''
                actions=[('Rotate',-2147483648,default),('Set',2,replacement),('IterateTwice',0,default),('Rotate',2147483647,default),('Get',0,default),('Get',-1,default)]
                with self.subTest(language=language,kind=kind):
                    case,observed=self.run_code(language,'inverse-offset',code,kind,initial,actions)
                    self.assertNotIn('error',observed);self.assertTrue(valid_observation('7.9',case,observed))
if __name__=='__main__':unittest.main()
