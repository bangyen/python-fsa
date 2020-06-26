import unittest
import automaton

class TestAuto(unittest.TestCase):

    def test_state(self):
        for base in range(2, 5):
            for num in range(2, 5):
                self.assertEqual(automaton.StateMach.div_by(base, num).state,
                                 'S0', "Divisibility FSAs should start at S0")

    def test_call_three(self):
        fsa = automaton.StateMach.div_by(2, 3)
        self.assertTrue(fsa(1, 1).accept, "Multiple args: 3 mod 3 (base 2)")
        self.assertTrue(fsa(0, 1, 1).accept, "Leading zero: 3 mod 3 (base 2)")
        self.assertTrue(fsa([1, 1]).accept, "List: 3 mod 3 (base 2)")
        self.assertTrue(fsa(1)(1).accept, "Multiple calls: 3 mod 3 (base 2)")

    def test_call_min(self):
        fsa = automaton.StateMach.div_by(2, 8).fsa_min()
        self.assertFalse(fsa(1, 1, 1, 0).accept, "Multiple args: 14 mod 8 (base 2)")
        self.assertFalse(fsa(0, 1, 1, 1, 0).accept, "Leading zero: 3 mod 5 (base 2)")
        self.assertFalse(fsa([1, 1, 1, 0]).accept, "List: 3 mod 5 (base 2)")
        self.assertFalse(fsa(1)(1)(1)(0).accept, "Multiple calls: 3 mod 5 (base 2)")

    def test_wiki_min(self):
        pre = {
            'S0': {0: 'S1', 1: 'S2', 'start': True, 'accept': False},
            'S1': {0: 'S0', 1: 'S3', 'start': False, 'accept': False},
            'S2': {0: 'S4', 1: 'S5', 'start': False, 'accept': True},
            'S3': {0: 'S4', 1: 'S5', 'start': False, 'accept': True},
            'S4': {0: 'S4', 1: 'S5', 'start': False, 'accept': True},
            'S5': {0: 'S5', 1: 'S5', 'start': False, 'accept': False}
        }
        post = {
            'S0': {0: 'S0', 1: 'S1', 'start': True, 'accept': False},
            'S1': {0: 'S1', 1: 'S2', 'start': False, 'accept': True},
            'S2': {0: 'S2', 1: 'S2', 'start': False, 'accept': False}
        }
        old = automaton.StateMach(pre).fsa_min()
        self.assertEqual(old.fsa, post, "DFA Minimization (Wikipedia Example)")
        self.assertEqual(old.accept, False, "S0 is not an accept state")
        self.assertEqual(old(1)(0).accept, True, "Multiple calls, S4 (new S1) is an accept state")
        self.assertEqual(old.fsa_min(), old, "Multiple calls, S4 (new S1) is an accept state")

    def test_malta_min(self):
        pre = {
            'S0': {'a': 'S1', 'b': 'S0', 'start': True, 'accept': True},
            'S1': {'a': 'S0', 'b': 'S2', 'start': False, 'accept': True},
            'S2': {'a': 'S2', 'b': 'S1', 'start': False, 'accept': False},
            'S3': {'a': 'S1', 'b': 'S2', 'start': False, 'accept': False}
        }
        post = {
            'S0': {'a': 'S1', 'b': 'S0', 'start': True, 'accept': True},
            'S1': {'a': 'S0', 'b': 'S2', 'start': False, 'accept': True},
            'S2': {'a': 'S2', 'b': 'S1', 'start': False, 'accept': False},
        }
        old = automaton.StateMach(pre).fsa_min()
        self.assertEqual(old.fsa, post, "DFA Minimization (Wikipedia Example)")
        self.assertTrue(old.accept, "S0 is not an accept state")
        self.assertFalse(old('a')('b').accept, "Multiple calls, S4 (new S1) is an accept state")
        self.assertEqual(old.fsa_min(), old, "Multiple calls, S4 (new S1) is an accept state")

    def test_combine(self):
        test = {
            'S0': {0: 'S0', 1: 'S1', 'start': True, 'accept': False},
            'S1': {0: 'S1', 1: 'S2', 'start': False, 'accept': True},
            'S2': {0: 'S2', 1: 'S2', 'start': False, 'accept': False}
        }
        combine = {
            '{S1,S2}': {0: ['S1', 'S2'], 1: 'S2', 'start': False, 'accept': True}
        }
        fsa = automaton.StateMach(test)
        self.assertEqual(fsa.combine('S1', 'S2'), combine, 'Combine function test')

    def test_str(self):
        table = 'S0: | 0: S0,	1: S1,	start: True ,	accept: True  |\n' \
            + 'S1: | 0: S2,	1: S0,	start: False,	accept: False |\n' \
            + 'S2: | 0: S1,	1: S2,	start: False,	accept: False |'
        self.assertEqual(str(automaton.StateMach.div_by(2, 3)), table, "String representation should be a table")

    def test_graph(self):
        graph = '''digraph {
            rankdir=LR size="8,5"
            "" [height=0 shape=none width=0]
            S0 [shape=doublecircle]
            "" -> S0 [arrowsize=0.75]
            S0 -> S1 [label="1,3,5,7,9" arrowsize=0.75]
            S0 -> S0 [label="0,2,4,6,8" arrowsize=0.75]
            S1 [shape=circle]
            S1 -> S1 [label="1,3,5,7,9" arrowsize=0.75]
            S1 -> S0 [label="0,2,4,6,8" arrowsize=0.75]
        }'''
        fsa = automaton.StateMach.div_by(10, 2)
        for line in graph.split():
            self.assertTrue(line in fsa.graph().source, "Graph function should combine arrows")


if __name__ == '__main__':
    unittest.main()
