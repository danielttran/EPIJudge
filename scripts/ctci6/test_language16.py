"""Precise text, substitution and keypad conventions."""
import unittest
from corpus16 import oracle,valid_observation

class LanguageContractTests(unittest.TestCase):
    def test_english_minimum_and_zero_groups_have_exact_spacing(self):
        self.assertEqual('Negative Two Billion One Hundred Forty Seven Million Four Hundred Eighty Three Thousand Six Hundred Forty Eight',oracle('16.8',[-2147483648]))
        self.assertEqual('One Million One',oracle('16.8',[1000001]))
        self.assertEqual('Zero',oracle('16.8',[0]))
        self.assertFalse(valid_observation('16.8',dict(expected='One Hundred Five'),dict(actual='One Hundred And Five',mutationOk=True)))
    def test_substitutions_can_be_empty_and_equal_but_must_consume_all_text(self):
        for pattern,text in (('ab','x'),('aa',''),('abba','xxxx'),('','')):self.assertTrue(oracle('16.18',[pattern,text]))
        for pattern,text in (('','x'),('aa','xxx'),('abba','x')):self.assertFalse(oracle('16.18',[pattern,text]))
        self.assertFalse(valid_observation('16.18',dict(expected=True),dict(actual=1,mutationOk=True)))
    def test_t9_exact_length_duplicate_order_and_four_letter_groups(self):
        self.assertEqual(['tree','used','tree'],oracle('16.20',['8733',['tree','used','true','tree']]))
        self.assertEqual(['p','q','r','s'],oracle('16.20',['7',list('abcdefghijklmnopqrstuvwxyz')]))
        self.assertEqual(['w','x','y','z'],oracle('16.20',['9',list('abcdefghijklmnopqrstuvwxyz')]))
        self.assertEqual([],oracle('16.20',['10',['a','tree']]))
        self.assertEqual([],oracle('16.20',['',['a']]))

if __name__=='__main__':unittest.main()
