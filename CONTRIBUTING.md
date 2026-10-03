# Contributing

Keep the library small, readable, and correct. Changes should improve a concrete
teaching example or application use case rather than duplicate the full feature
sets of established automata toolkits.

## Local checks

Use Python 3.10 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make check
python examples/teaching.py
make build
```

For a correctness fix, add a regression with the smallest machine that exposes
it. For conversion or minimization changes, compare acceptance before and after
across exhaustive short words. Keep examples executable and document mutation,
missing-transition, and empty-input behavior. CI verifies the supported Python
versions; local checks only verify the interpreter you run them under.

## Release checklist

1. Run all checks and examples, and review the CI matrix results.
2. Update the version in both `pyproject.toml` and `src/python_fsa/__init__.py`.
3. Build the source distribution and wheel with `python -m build`.
4. Install the wheel into a clean environment and run acceptance checks from
   outside the repository. Verify that `py.typed` is included.
5. Document API changes and compatibility limits in release notes.
6. Publish only after reviewing the built artifacts and release notes.

This revision raises the Python minimum from 3.8 to 3.10, normalizes integer input
keys to strings, and gives NFA execution a set of active states. Existing DFA
streaming and method aliases remain available. Consumers reading NFA `state`
should use `active_states` for a consistent set-valued interface.
