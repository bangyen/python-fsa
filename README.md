# Python State Machine
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f7f5afb6b8414c74b4ea46cf3d49cb34)](https://app.codacy.com/manual/bangyen99/python-fsa?utm_source=github.com&utm_medium=referral&utm_content=bangyen/python-fsa&utm_campaign=Badge_Grade_Dashboard)
[![CodeFactor](https://www.codefactor.io/repository/github/bangyen/python-fsa/badge)](https://www.codefactor.io/repository/github/bangyen/python-fsa)\
A Python class implementation of deterministic finite-state machines.

# Format
Using an finite-state automaton that checks if a binary number is divisible by three as an example,
FSAs will be represented as follows:
```python
divisible = {
    'S0': {0: 'S0', 1: 'S1', 'start': True, 'accept': True},
    'S1': {0: 'S2', 1: 'S0', 'start': False, 'accept': False},
    'S2': {0: 'S1', 1: 'S2', 'start': False, 'accept': False}
}
```
Each key represents a different state, and each value contains a dictionary
with the following information: the new state upon reception of a particular input,
whether a state is the starting state, and whether a state is an accepting state.

Additionally, the matrix representation of the directed graph corresponding to
the aforementioned FSA is as follows:
```python
div_matrix = [
    [0, 1, ()],
    [1, (), 0],
    [(), 0, 1]
]
```
The ij-th entry indicates which symbols cause a transition from the i-th state to the j-th state.
If an entry is the empty tuple, nothing causes a transition between the two.
Notation adapted from:
'Generalized transition matrix of a sequential machine and its applications' - T.Kameda
