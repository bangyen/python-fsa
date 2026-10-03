# Changelog

## 2.0.0 — release candidate

This version focuses on correct execution, readable automata algorithms, and
teaching tools. Release artifacts are prepared; this entry does not imply a
published package or GitHub release.

### Compatibility changes

- Python 3.10 is now the minimum supported version; CI covers 3.10–3.14.
- Integer transition keys are normalized to strings. A state cannot define both
  `1` and `"1"`; they represent the same input symbol.
- NFA execution can have multiple active states. `state` is a string when one
  state is active and a frozenset otherwise. Use `active_states` for a consistent
  set-valued interface.
- State names must be strings, flags must be booleans, and transition targets
  must be valid state names. `start` and `accept` cannot be processed as inputs.
- DFA minimization resets execution when it performs minimization and completes
  partial transition tables with a rejecting sink. Acceptance is preserved,
  while missing transitions become explicit transitions.
- Direct NFA minimization now raises `MinimizationError`; call
  `nfa.to_dfa().minimize()` instead.

### Added

- NFA execution with branching, missing transitions, and empty destination sets.
- `to_dfa()` for reachable-subset conversion to a complete DFA.
- `reset()` and independent `accepts(sequence)` checks.
- `trace(sequence)` for input-by-input execution explanations.
- `minimization_trace()` for partition groups, destination-group signatures,
  and the stable equivalence classes. Both trace methods leave the original
  machine unchanged.
- An executable teaching tutorial, contribution guide, and release checklist.
- Regression and exhaustive short-word language-equivalence tests.
- Wheel installation checks and executable examples in CI.

### Fixed

- Reachability starts from the declared start state rather than the current
  execution state.
- Minimization preserves the start state when equivalent states merge and no
  longer fails when the current execution state is merged away.
- Streaming updates acceptance after every successful symbol, including when
  a later symbol in the same batch fails.
- NFA visualization draws every destination and can group list-valued targets.
- Symbol normalization prevents mixed integer/string label sorting failures.
- Public exception exports and typing metadata are included in packages.

### Migration example

```python
from python_fsa import StateMachine

machine = StateMachine.create_divisibility_checker(2, 3)
assert machine.accepts([1, 1])  # Independent check from the start
machine.reset()(1)(1)          # Stateful streaming still supports chaining
assert machine.accept

# For an NFA, inspect nfa.active_states and minimize via nfa.to_dfa().minimize().
```

Epsilon transitions remain unsupported, and subset construction can grow
exponentially. The project targets small explicit machines and teaching use.
