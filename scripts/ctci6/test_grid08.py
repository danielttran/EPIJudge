"""Contract counterexamples for paths, legal tower moves, and four-neighbor fill."""
import unittest
from corpus08 import oracle, valid_observation

class GridContractTests(unittest.TestCase):
    def test_any_right_down_path_not_just_oracle_choice(self):
        case=dict(arguments=[[[1,1],[1,1]]],expected=[[0,0],[1,0],[1,1]])
        self.assertTrue(valid_observation('8.2',case,dict(actual=[[0,0],[0,1],[1,1]],mutationOk=True)))
        for path in ([], [[0,0],[1,1]], [[0,0],[0,1],[0,0],[1,0],[1,1]], [[0,0],[0,2],[1,1]], [[0,0],[True,0],[1,1]]):
            self.assertFalse(valid_observation('8.2',case,dict(actual=path,mutationOk=True)))
        self.assertFalse(valid_observation('8.2',case,dict(actual=case['expected'],mutationOk=False)))
        blocked=dict(arguments=[[[1,0],[0,1]]],expected=[])
        self.assertFalse(valid_observation('8.2',blocked,dict(actual=[[0,0],[1,1]],mutationOk=True)))
        self.assertTrue(valid_observation('8.2',blocked,dict(actual=[],mutationOk=True)))

    def test_hanoi_oracle_transcripts_obey_stack_rules_and_bound(self):
        for count in range(13):
            towers=[list(range(count,0,-1)),[],[]]
            moves=oracle('8.6',[count]);self.assertEqual((1<<count)-1,len(moves))
            for disk,source,destination in moves:
                self.assertNotEqual(source,destination)
                self.assertEqual(disk,towers[source][-1])
                self.assertTrue(not towers[destination] or towers[destination][-1]>disk)
                towers[destination].append(towers[source].pop())
            self.assertEqual([[],[],list(range(count,0,-1))],towers)
        case=dict(arguments=[2],expected=oracle('8.6',[2]))
        for moves in ([[2,0,2],[1,0,2]],case['expected'][::-1],[]):
            self.assertFalse(valid_observation('8.6',case,dict(actual=moves,mutationOk=True)))

    def test_fill_excludes_diagonals_and_preserves_other_colors(self):
        args=[[[1,0],[0,1]],0,0,2]
        self.assertEqual([[2,0],[0,1]],oracle('8.10',args))
        case=dict(arguments=args,expected=oracle('8.10',args))
        self.assertFalse(valid_observation('8.10',case,dict(actual=[[2,0],[0,2]],mutationOk=True)))
        self.assertFalse(valid_observation('8.10',case,dict(actual=case['expected'],mutationOk=False)))
        for r,c in ((-2147483648,0),(0,2147483647)):
            self.assertEqual([[1]],oracle('8.10',[[[1]],r,c,2]))
        self.assertEqual([[1]],oracle('8.10',[[[1]],0,0,1]))


class FillRuntimeTests(unittest.TestCase):
    def test_correct_values_in_a_copy_cannot_replace_input_mutation(self):
        import json
        from core import ROOT
        from verify01 import execute
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='8.10')
        config=entry['languages']['python']
        source=config['prefix']+config['solutionCode']+'''
_original=PaintFill
def PaintFill(screen,row,column,newColor):
    return _original([line.copy() for line in screen],row,column,newColor)
'''
        observation=execute('python',False,[dict(ref='8.10',arguments=[[[1,1]],0,0,2])],ROOT/'.epi-runs/ctci6-fill-copy-negative',source_builder=lambda *_:config['harness'],companion_files={'solution.py':source})[0]['observation']
        self.assertEqual([[2,2]],observation['actual'])
        self.assertFalse(observation['mutationOk'])

    def test_replacing_a_row_by_equal_values_is_not_preservation(self):
        import json
        from core import ROOT
        from verify01 import execute
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='8.10')
        config=entry['languages']['python']
        source=config['prefix']+config['solutionCode']+'''
_original=PaintFill
def PaintFill(screen,row,column,newColor):
    _original(screen,row,column,newColor)
    screen[0]=screen[0].copy()
    return screen
'''
        observation=execute('python',False,[dict(ref='8.10',arguments=[[[1,1]],0,0,2])],ROOT/'.epi-runs/ctci6-fill-row-negative',source_builder=lambda *_:config['harness'],companion_files={'solution.py':source})[0]['observation']
        self.assertEqual([[2,2]],observation['actual'])
        self.assertFalse(observation['mutationOk'])

if __name__=='__main__':unittest.main()
