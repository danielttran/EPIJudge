"""Reference Python operation semantics and exact all-rank node bijection."""
from collections import Counter
import random
import unittest
from algorithms_random04 import body
from models_random04 import NODE,RANDOM
from corpus_random04 import oracle,transcript,valid_observation,transitions

class RandomBstReferenceTests(unittest.TestCase):
    def test_updates_and_every_rank_preserve_actual_duplicate_node_identity(self):
        namespace={};exec(NODE['python']+RANDOM['python']+body('python'),namespace)
        actor=namespace['RandomBst']();source=namespace['RandomSource'];expected=Counter();rng=random.Random(411)
        def check_state():
            stack=[];node=actor.Root;ordered=[];seen=set()
            while node is not None or stack:
                while node is not None:
                    self.assertNotIn(id(node),seen);seen.add(id(node));stack.append(node);node=node.Left
                node=stack.pop();ordered.append(node);node=node.Right
            self.assertEqual(sorted(expected.elements()),[node.Data for node in ordered])
            for rank,wanted in enumerate(ordered):
                calls=[]
                def draw(lower,upper):calls.append((lower,upper));return rank
                source.Draw=staticmethod(draw)
                self.assertIs(wanted,actor.GetRandomNode());self.assertEqual([(0,len(ordered)-1)],calls)
            if not ordered:self.assertIsNone(actor.GetRandomNode())
            for value in range(-3,4):
                found=actor.Find(value);self.assertEqual(expected[value]>0,found is not None)
                if found is not None:self.assertIn(id(found),seen);self.assertEqual(value,found.Data)
        for _ in range(150):
            value=rng.randrange(-3,4)
            if rng.randrange(3):actor.Insert(value);expected[value]+=1
            else:
                present=expected[value]>0;self.assertEqual(present,actor.Delete(value))
                if present:expected[value]-=1
            check_state()
        for value in list(expected.elements()):self.assertTrue(actor.Delete(value));expected[value]-=1
        check_state()
    def test_transcript_oracle_does_not_prescribe_one_random_choice(self):
        args=transcript([('Insert',1),('Insert',2),('GetRandomNode',None)]);expected,changes=transitions(args)
        for value in (1,2):
            actual={'results':[None,None,None,[value]],'finalValues':[1,2]}
            self.assertTrue(valid_observation('4.11',dict(arguments=args,expected=expected),dict(actual=actual,changes=changes,mutationOk=True,uniformOk=True)))
        bad=[dict(row) for row in changes];bad[1]=dict(added=[],removed=[],count=0)
        self.assertFalse(valid_observation('4.11',dict(arguments=args,expected=expected),dict(actual=actual,changes=bad,mutationOk=True,uniformOk=True)))

if __name__=='__main__':unittest.main()
