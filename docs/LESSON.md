# From branching execution to a minimal DFA

A 40–50 minute lesson for learners who know basic Python dictionaries and loops.
No prior automata course is required. By the end, you should be able to explain
how an NFA tracks possible paths, how a DFA represents those paths as one state,
and why equivalent DFA states can merge.

You need Python 3.10+ and this repository. No diagram rendering is required.

## 1. Set up and define the goal (5 minutes)

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install .
python examples/lesson_exercises.py
```

If you already have the 2.0.0 release wheel installed, you can skip installation.
This lesson uses the 2.0.0 API. Do not install `python-fsa` by name from PyPI:
that name belongs to another project.

The exercise command prints prompts; it does not ask for answers interactively.
Open `examples/lesson_exercises.py` in your editor and replace the `None` values
in `PREDICTIONS` as you work. Later, `--check` validates your saved answers.

Our machine recognizes words over the alphabet `{a, b}` that contain `ab`.
For example, `baab` matches, but `bbaa` does not. A word is a sequence of input
symbols; the empty word has no symbols. A state records what the machine knows
about the input so far. An accepting state means the word may end successfully
at that point.

Before running the answers, predict the results for the empty word, `a`, `ab`,
`baab`, and `bbaa`. Record your predictions in `PREDICTIONS` inside
`examples/lesson_exercises.py`.

## 2. Follow the NFA branches (10 minutes)

The machine definition appears in `containing_ab()` in the exercise script:

| State | Meaning | On `a` | On `b` | Accepting? |
|---|---|---|---|---|
| S0 | Keep searching for the start of `ab` | S0 and S1 | S0 | No |
| S1 | An `a` could be the beginning of a match | The S1 path dies | S2 | No |
| S2 | An `ab` has already matched | S2 | S2 | Yes |

`S0` is the start state. An NFA can follow multiple paths at once. On `a`, it
both keeps searching and remembers a possible match start. A missing transition
kills only that path. Acceptance requires at least one accepting active state.

Run the walkthrough:

```bash
python examples/teaching.py
```

Read the execution trace for `baab` before the partition output. Work through
these configurations:

| Prefix read | Active states | Explanation |
|---|---|---|
| Empty | S0 | Nothing has matched |
| b | S0 | Keep searching |
| ba | S0, S1 | Search continues; an `a` may start the match |
| baa | S0, S1 | The previous S1 path dies; the latest `a` creates a new one |
| baab | S0, S2 | One path has found `ab`, so the word accepts |

Now predict the active states after `a` and `ab`. Enter sorted lists of state
names in the exercise file. Explain why `S1` disappears when another `a` arrives.

For your own experiments, use `accepts(word)` for an independent check and
`trace(word)` for an explanation. Both start fresh and leave the machine alone.
Calling `machine(*word)` streams input and changes its active states;
`machine.reset()` starts that stream over.

## 3. Replace sets of paths with DFA states (10 minutes)

`nfa.to_dfa()` assigns one DFA state to each reachable subset of NFA states.
Every input now has exactly one destination. A complete DFA also has a rejecting
empty-subset state if such a subset is reachable; this example does not need one.

In the tutorial's converted DFA:

| DFA state | NFA subset | Accepting? |
|---|---|---|
| S0 | {S0} | No |
| S1 | {S0, S1} | No |
| S2 | {S0, S2} | Yes |
| S3 | {S0, S1, S2} | Yes |

These names belong to different machines. DFA `S1` represents a whole NFA
subset; it is not the same thing as NFA `S1`. The names above reflect this
example's conversion order. Do not assume the same numbering for other machines.

Predict the number of reachable DFA states. Why is `{S1}` never reached alone?
Why do we not need all eight possible subsets of the three NFA states?

## 4. Explain the state merges (10 minutes)

An accepting state and a rejecting state cannot merge: the empty suffix already
distinguishes them. Begin with two groups:

- Group 0: `[S2, S3]` (accepting)
- Group 1: `[S0, S1]` (rejecting)

The trace alphabet is `['a', 'b']`. A state's signature lists the group reached
on `a`, then the group reached on `b`.

| DFA state | Initial signature |
|---|---|
| S0 | [1, 1] |
| S1 | [1, 0] |
| S2 | [0, 0] |
| S3 | [0, 0] |

`S0` and `S1` split because input `b` takes them to groups with different
acceptance. The word `b` is a distinguishing suffix. `S2` and `S3` stay together:
all future input remains within the accepting group.

After splitting, the groups are `[S2, S3]`, `[S0]`, and `[S1]`. Their indices have
changed, so signatures must be recomputed. The next round is stable: within each
group, every state's signature agrees. The minimized DFA has three states.

Fill in the final two predictions: the minimal state count and the converted
DFA states that merge. Run:

```bash
python examples/lesson_exercises.py --check
```

A wrong or missing prediction produces a nonzero exit status and a hint. Revise
your explanation before checking the worked answers:

```bash
python examples/lesson_exercises.py --answers
```

The script also checks all 127 words of length zero through six against the
plain-language condition `"ab" in word`. This finite check is useful evidence;
it does not prove equivalence for every possible word. The conversion and
refinement algorithms provide the general argument.

## 5. Transfer the idea (5–10 minutes)

Design a DFA that accepts words ending in `ab`, rather than containing `ab`.
Reuse three states, but make a match disappear when the ending changes:

Write the definition yourself before checking the [reference solution](LESSON_ANSWERS.md).
Check that `baab` accepts and `abba` rejects. Explain why `abba` distinguishes
the two languages, find a second distinguishing word, and inspect your
machine's `trace("abba")`.

## Check your explanations

After making your predictions and attempting the transfer exercise, compare
with the [worked answers and reference DFA](LESSON_ANSWERS.md).

## Learner feedback

After trying the lesson, record feedback using [LEARNER_FEEDBACK.md](LEARNER_FEEDBACK.md).
Focus on the first confusing step, your prediction before seeing the output,
and the wording or output that would have helped. No learner feedback has been
collected yet; executing the scripts verifies behavior, not teaching effectiveness.
