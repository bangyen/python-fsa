# Lesson answers

Attempt the predictions and transfer task in [the lesson](LESSON.md) before
reading these solutions.

## Worked explanations

- The empty word rejects because the initial active set contains only S0.
- After `a`, the active set is `[S0, S1]`; after `ab`, it is `[S0, S2]`.
- `bbaa` rejects; `baab` accepts.
- The converted DFA has four reachable states. S0 is always active in the NFA,
  so a subset containing only S1 cannot be reached.
- Minimization merges converted DFA S2 and S3, leaving three states. Both
  remember that a match already happened, and neither can lose that fact.
- `abba` contains `ab` but does not end in `ab`. `aba` is another example.

## Reference DFA: words ending in ab

```python
from python_fsa import StateMachine

ending_ab = StateMachine({
    "S0": {"a": "S1", "b": "S0", "start": True, "accept": False},
    "S1": {"a": "S1", "b": "S2", "start": False, "accept": False},
    "S2": {"a": "S1", "b": "S0", "start": False, "accept": True},
})
assert ending_ab.accepts("baab")
assert not ending_ab.accepts("abba")
```

Explain why `abba` distinguishes the two languages. Find a second distinguishing
word, and check it with both machines. Then inspect `ending_ab.trace("abba")`.

