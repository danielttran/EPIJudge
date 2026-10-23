import unittest
from corpus_xml16 import oracle,fixture

class XmlEncodingTests(unittest.TestCase):
    def test_empty_leaf_and_empty_tree(self):
        self.assertEqual(['7','0','0'],oracle('16.12',fixture([])))
        self.assertEqual([],oracle('16.12',[[],[],[],[],[],[],['node'],[1]]))
    def test_literal_spaces_are_one_token_and_owner_order_is_preserved(self):
        args=fixture([0,0]);args[3:6]=[[2,0,1,0],['key','key','other','other'],['Last','A B','',' ']]
        self.assertEqual(['7','2','A B','9',' ','0','7','9','','0','0','7','2','Last','0','0','0'],oracle('16.12',args))
    def test_text_is_before_exit_and_children_are_in_sibling_order(self):
        args=[['node','other','node'],['','First','Second'],[[1,2],[],[]],[],[],[],['node','other'],[7,9]]
        self.assertEqual(['7','0','9','0','First','0','7','0','Second','0','0'],oracle('16.12',args))
    def test_deep_tree_does_not_require_recursive_python_calls(self):
        args=fixture(list(range(999)));actual=oracle('16.12',args)
        self.assertEqual(3000,len(actual));self.assertEqual(1000,actual.count('7'));self.assertEqual(2000,actual.count('0'))

if __name__=='__main__':unittest.main()
