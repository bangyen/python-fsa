# Python FSA

[![CI](https://github.com/bangyen/python-fsa/workflows/CI/badge.svg)](https://github.com/bangyen/python-fsa/actions)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

A small Python 3.10+ library for learning and experimenting with finite state
automata. Define a machine using dictionaries, process inputs, inspect execution
steps, convert NFAs to DFAs, minimize DFAs, and draw state diagrams.

The project focuses on readable algorithms and classroom-sized examples. It is
useful for teaching, arithmetic experiments, and applications needing a small
explicit automaton. It does not claim to replace broader formal-language tools
such as automata-lib, pyformlang, or FAdo.

For changes and migration from 1.x, see [CHANGELOG.md](CHANGELOG.md).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install .
```

Download the wheel from the [2.0.0 GitHub release](https://github.com/bangyen/python-fsa/releases/tag/v2.0.0)
and install it with `python -m pip install python_fsa-2.0.0-py3-none-any.whl`.
The `python-fsa` name on PyPI belongs to a different project; installing it by
name from PyPI does not install this repository.

The Python Graphviz package is installed automatically. Rendering diagrams also
requires the Graphviz system executable (`dot`); inspecting `.source` does not.

For development:

```bash
python -m pip install -e ".[dev]"
pre-commit install
make check
```

## Independent checks and streaming

```python
from python_fsa import StateMachine

machine = StateMachine.create_divisibility_checker(base=2, divisor=3)
assert machine.accepts([1, 1])       # Binary 11 = 3
assert not machine.accepts([1, 0, 1])  # Binary 101 = 5

# accepts() always starts fresh and leaves execution state unchanged.
# Calling the machine processes a stream and changes its execution state.
machine(1)(1)
assert machine.accept
machine.reset()
assert machine.state == "S0"
```

`machine(*symbols)` and `machine([symbols])` both support chaining. Pass a word
as `machine(*"ab")`, or use `machine.accepts("ab")` for an independent check.
A plain `machine("ab")` processes a single symbol named `ab`.

## Define an automaton

```python
machine = StateMachine({
    "waiting": {"a": "seen_a", "b": "waiting", "start": True, "accept": False},
    "seen_a": {"a": "seen_a", "b": "matched", "start": False, "accept": False},
    "matched": {"a": "seen_a", "b": "waiting", "start": False, "accept": True},
})
assert machine.accepts("aab")
assert not machine.accepts("aba")
```

Definitions require exactly one start state and boolean `start`/`accept` flags
on every state. Targets must reference existing states. State names are normalized
to `S0`, `S1`, etc.; input symbols are normalized to strings, so `1` and `"1"`
represent the same input. Defining both keys in one state is rejected.
`start` and `accept` are reserved metadata keys and cannot be input symbols.
The constructor copies the definition. Treat the public `fsa` dictionary as
read-only; construct a new machine to change the transition structure.

## NFAs and conversion

```python
nfa = StateMachine({
    "S0": {"a": ["S0", "S1"], "b": "S0", "start": True, "accept": False},
    "S1": {"b": "S2", "start": False, "accept": False},
    "S2": {"a": "S2", "b": "S2", "start": False, "accept": True},
})
assert nfa.accepts("baab")  # Contains ab
assert not nfa.accepts("bbaa")

dfa = nfa.to_dfa()
minimal = dfa.minimize()
assert minimal.accepts("baab")
```

NFA execution tracks all possible destinations in `active_states`, a frozenset.
A word is accepted if any active state accepts it. Missing NFA transitions and
empty destination lists eliminate that branch; an empty active set rejects.
`state` is a string when exactly one state is active and a frozenset otherwise.
Use `active_states` when writing code that handles both DFAs and NFAs.

`to_dfa()` starts from the declared start state and constructs reachable subsets.
It returns a new complete DFA, including a rejecting sink when needed.
Subset construction may produce exponentially many states, so this library is
intended for small machines. Epsilon transitions are not supported; an empty
string key is an ordinary input symbol.

## Teaching: inspect each step

```python
for step in nfa.trace("ab"):
    print(step)
# {'symbol': None, 'states': ['S0'], 'accept': False}
# {'symbol': 'a', 'states': ['S0', 'S1'], 'accept': False}
# {'symbol': 'b', 'states': ['S0', 'S2'], 'accept': True}
```

`trace()` includes the initial configuration and one record per input, without
changing the original machine. This makes it suitable for notebooks, lessons,
and explaining why a word was accepted. Run `python examples/teaching.py` for a
complete example comparing an NFA, its DFA, and its minimal DFA.

DFA minimization uses partition refinement:

1. Complete the transition table and retain reachable states.
2. Separate accepting and rejecting states.
3. Split each group by the groups reached on every input symbol.
4. Repeat until no group splits, then replace each group with one state.

The implementation favors clarity over large-scale performance. Regression tests
compare accepted languages over exhaustive short words and check divisibility
machines against integer arithmetic.

## Execution and error semantics

- `reset()` returns to the declared start state.
- `accepts(sequence)` starts fresh, returns a boolean, and never changes the original.
  Undefined DFA transitions reject the word.
- Streaming a missing DFA transition raises `InvalidTransitionError`. Successfully
  processed earlier symbols remain committed, with `accept` kept consistent.
- `trace(sequence)` raises on an undefined DFA transition, identifying the failing
  step through the exception's `from_state` and `input_symbol` attributes.
- `minimize()` changes the DFA in place and resets execution when it performs
  minimization. Repeated calls on an already minimized DFA return the same object.
  Convert an NFA first; direct NFA minimization raises `MinimizationError`.
- Partial DFAs are supported; minimization completes missing transitions with a
  rejecting sink. The result preserves acceptance behavior, though missing
  transitions become explicit transitions.
- `remove_unreachable_states()` uses the declared start state, regardless of
  how much input has been processed.

All public exceptions are exported from `python_fsa`: `FSAError`,
`InvalidFSADefinitionError`, `InvalidStateError`, `InvalidTransitionError`,
and `MinimizationError`.

## Visualization and compatibility

```python
machine.create_graph().render("automaton", format="svg", cleanup=True)
print(machine.create_graph().source)
```

`create_graph()` handles DFA and NFA edges, combines equivalent edge labels by
default, and supports `add_spaces=True` and `circular_layout=True`.
`combine_states(*names)` returns one combined state definition; it does not
convert a whole NFA. Use `to_dfa()` for conversion.

Legacy aliases remain available: `div_by`, `combine`, `norm`, `arrow_min`,
`remove`, `fsa_min`, and `graph`.

## Maintenance and scope

CI checks Python 3.10–3.14, lint, formatting, type checking, tests, and installation
from a built wheel. Run `make check` locally and `make build` to produce packages.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the development and release workflow.

`machine.minimization_trace()` explains partition refinement without mutation.
It returns the reachable, completed DFA definition, its alphabet, and refinement
rounds. Each round lists groups and a transition signature for each state:
the destination group indices in alphabet order. Within a group, different
signatures cause a split; the final round is marked `stable=True`.
Names refer to the returned definition, which can differ from the original
machine after conversion and removal of unreachable states.

Future work should serve a demonstrated teaching or application need. Useful
candidates include epsilon closure and machine
serialization. Broad regex/grammar tooling and high-performance automata are
outside the current scope. Bug reports should include a machine definition,
input sequence, expected result, and actual result.

Licensed under GPL-3.0; see [LICENSE](LICENSE).
