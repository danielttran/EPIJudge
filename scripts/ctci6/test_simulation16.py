"""Arithmetic restrictions are structural checks; numerical behavior is executed separately."""
import re
import unittest
from algorithms16 import body
from core import LANGUAGES
from corpus16 import oracle,valid_observation

class SimulationContractTests(unittest.TestCase):
    def test_addition_only_bodies_do_not_use_other_arithmetic_operators(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                code=body('16.9',language)
                code=re.sub(r'(?<!\w)-1(?!\d)','UNIT_NEGATIVE',code)
                self.assertIsNone(re.search(r'[-*/%&|^~]|<<|>>',code))
                self.assertNotRegex(code,r'\b(abs|Abs|Math|math)\b')
    def test_arithmetic_signs_truncation_and_endpoints(self):
        for a,b,op,expected in ((-7,3,'divide',-2),(7,-3,'divide',-2),(-7,-3,'divide',2),(-4,-3,'multiply',12),(0,-3,'multiply',0),(-10000,10000,'subtract',-20000),(-10000,-10000,'multiply',100000000)):
            self.assertEqual(expected,oracle('16.9',[a,b,op]))
        self.assertFalse(valid_observation('16.9',dict(expected=-2),dict(actual=-3,mutationOk=True)))
    def test_ant_turn_flip_move_order_and_erased_white_extent(self):
        expected=[['R'],['#','D'],['.#','L#'],['U#','##'],['#R','##'],['.U','#.','##']]
        for steps,board in enumerate(expected):self.assertEqual(board,oracle('16.22',[steps]))
        self.assertFalse(valid_observation('16.22',dict(expected=['.#','L#']),dict(actual=['R#','.#'],mutationOk=True)))

if __name__=='__main__':unittest.main()
