"""Independent mask enumeration checks the actual duplicate-lifting observer."""
from collections import defaultdict
from fractions import Fraction
import itertools
import unittest
from harness_subset13_python import CORE
from models13 import COINS
from corpus_subset13 import valid_observation

class SubsetMaskTests(unittest.TestCase):
    def test_actual_lift_is_uniform_over_independently_enumerated_compatible_masks(self):
        class NeedBit(Exception):pass
        for values in itertools.product((7,9),repeat=3):
            groups=defaultdict(list)
            for mask in range(8):groups[tuple(v for i,v in enumerate(values) if mask>>i&1)].append(mask)
            for output,masks in groups.items():
                namespace={'ChoiceBitSource':object,'RandomSubset':lambda values,coins: list(output)}
                exec(COINS['python']+CORE,namespace);state=namespace['SubsetState13'];state.Input=list(values)
                pending=[([],Fraction(1))];probabilities=defaultdict(Fraction);unresolved=Fraction()
                while pending:
                    prefix,mass=pending.pop()
                    class Bits:
                        index=0
                        def Next(self):
                            if self.index==len(prefix):raise NeedBit()
                            result=prefix[self.index];self.index+=1;return result
                    try:probabilities[state.mask(Bits())]+=mass
                    except NeedBit:
                        if len(prefix)==12:unresolved+=mass
                        else:
                            for bit in (0,1):pending.append((prefix+[bit],mass/2))
                self.assertTrue(set(probabilities)<=set(masks));self.assertGreater(sum(probabilities.values()),Fraction(98,100))
                for mask in masks:self.assertLessEqual(probabilities[mask],Fraction(1,len(masks)));self.assertGreaterEqual(probabilities[mask]+unresolved,Fraction(1,len(masks)))
    def test_grading_accepts_any_ordered_subset_but_not_reordering_or_ungrounded_flags(self):
        case=dict(arguments=[[7,7,9],[]],expected=[7,9])
        for actual in ([],[7],[7,7],[7,9],[7,7,9],[9]):self.assertTrue(valid_observation('13.8',case,dict(actual=actual,mutationOk=True,uniformOk=True)))
        for actual in ([9,7],[7,7,7],[8],[True]):self.assertFalse(valid_observation('13.8',case,dict(actual=actual,mutationOk=True,uniformOk=True)))
        self.assertFalse(valid_observation('13.8',case,dict(actual=[],mutationOk=True,uniformOk=False)))
if __name__=='__main__':unittest.main()
