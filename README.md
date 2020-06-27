# Python State Machine
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f7f5afb6b8414c74b4ea46cf3d49cb34)](https://app.codacy.com/manual/bangyen99/python-fsa?utm_source=github.com&utm_medium=referral&utm_content=bangyen/python-fsa&utm_campaign=Badge_Grade_Dashboard)
[![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen)](https://www.codacy.com/manual/bangyen99/python-fsa?utm_source=github.com&utm_medium=referral&utm_content=bangyen/python-fsa&utm_campaign=Badge_Coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) \
A Python class implementation of deterministic finite-state machines.

## Format
Using an finite-state automaton that checks if a binary number is divisible by three as an example, DFAs will be represented as follows:
```python
divisible = {
    'S0': {0: 'S0', 1: 'S1', 'start': True , 'accept': True },
    'S1': {0: 'S2', 1: 'S0', 'start': False, 'accept': False},
    'S2': {0: 'S1', 1: 'S2', 'start': False, 'accept': False}
}
```
Each key represents a different state, and each value contains a dictionary with the following information: the new state upon reception of a particular input, whether a state is the starting state, and whether a state is an accepting state. For NFAs, if an input has multiple new states, the new states will be represented as a list. ε-moves will be represented as a new key.

Additionally, the matrix representation of the directed graph corresponding to the aforementioned FSA is as follows:
```python
div_matrix = [
    [0, 1, ()],
    [1, (), 0],
    [(), 0, 1]
]
```
The ij-th entry indicates which symbols cause a transition from the i-th state to the j-th state. If an entry is the empty tuple, nothing causes a transition between the two. Notation adapted from: 'Generalized transition matrix of a sequential machine and its applications' - T.Kameda

## Methods
| Name      | Functionality                                                                                     |
|-----------|---------------------------------------------------------------------------------------------------|
| `div_by`  | Creates a StateMach object that determines if a number in a given `base` is divisible by `num`.   |
| `combine` | Combines the given NFA states into one state.                                                     |
| `fsa_min` | Minimizes a DFA by using the table-filling algorithm.                                             |
| `remove`  | Removes unreachable states of an FSA.                                                             |
| `graph`   | Creates a Graphviz Digraph object representing the FSA.                                           |
| `norm`    | Normalizes the FSA by renaming states to fit the aforementioned convention.                       |

## Future Updates
-   [ ] Powerset construction
-   [ ] ε-closures
-   [x] NFA state combination
-   [x] Transition matrices
