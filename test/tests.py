import unittest
import automaton

class TestAuto(unittest.TestCase):
    def test_state(self):
        self.assertEqual(automaton.StateMach.div_by(2, 3).state, 'S0', "Divisibility FSAs should start at S0")
        self.assertEqual(automaton.StateMach.div_by(2, 4).state, 'S0', "Divisibility FSAs should start at S0")
        self.assertEqual(automaton.StateMach.div_by(2, 5).state, 'S0', "Divisibility FSAs should start at S0")

    def test_call_three(self):
        fsa = automaton.StateMach.div_by(2, 3)
        self.assertEqual(fsa(1, 1).accept, True, "Multiple args: 3 mod 3 (base 2)")
        self.assertEqual(fsa(0, 1, 1).accept, True, "Leading zero: 3 mod 3 (base 2)")
        self.assertEqual(fsa([1, 1]).accept, True, "List: 3 mod 3 (base 2)")
        self.assertEqual(fsa(1)(1).accept, True, "Multiple calls: 3 mod 3 (base 2)")

    def test_call_min(self):
        fsa = automaton.StateMach.div_by(2, 8).fsa_min()
        self.assertEqual(fsa(1, 1, 1, 0).accept, False, "Multiple args: 14 mod 8 (base 2)")
        self.assertEqual(fsa(0, 1, 1, 1, 0).accept, False, "Leading zero: 3 mod 5 (base 2)")
        self.assertEqual(fsa([1, 1, 1, 0]).accept, False, "List: 3 mod 5 (base 2)")
        self.assertEqual(fsa(1)(1)(1)(0).accept, False, "Multiple calls: 3 mod 5 (base 2)")

    def test_wiki_min(self):
        pre = {
            'S0': {0: 'S1', 1: 'S2', 'start': True , 'accept': False},
            'S1': {0: 'S0', 1: 'S3', 'start': False, 'accept': False},
            'S2': {0: 'S4', 1: 'S5', 'start': False, 'accept': True },
            'S3': {0: 'S4', 1: 'S5', 'start': False, 'accept': True },
            'S4': {0: 'S4', 1: 'S5', 'start': False, 'accept': True },
            'S5': {0: 'S5', 1: 'S5', 'start': False, 'accept': False}
        }
        post = {
            'S0': {0: 'S0', 1: 'S1', 'start': True , 'accept': False},
            'S1': {0: 'S1', 1: 'S2', 'start': False, 'accept': True },
            'S2': {0: 'S2', 1: 'S2', 'start': False, 'accept': False}
        }
        old = automaton.StateMach(pre).fsa_min()
        self.assertEqual(old.fsa, post, "DFA Minimization (Wikipedia Example)")
        self.assertEqual(old.accept, False, "S0 is not an accept state")
        self.assertEqual(old(1)(0).accept, True, "Multiple calls, S4 (new S1) is an accept state")

if __name__ == '__main__':
    unittest.main()
