"""Prediction exercises for docs/LESSON.md; run with --help for options."""

import argparse
from itertools import product
from typing import Any

from python_fsa import StateMachine

# Fill these in after reading the lesson. Use bools, lists of state names,
# or integers as requested. Then run: python examples/lesson_exercises.py --check
PREDICTIONS: dict[str, Any] = {
    "empty_word": None,
    "after_a": None,
    "after_ab": None,
    "accepts_bbaa": None,
    "accepts_baab": None,
    "dfa_states": None,
    "minimal_states": None,
    "merged_states": None,
}

QUESTIONS = {
    "empty_word": "Does the NFA accept the empty word? (bool)",
    "after_a": "Which NFA states are active after 'a'? (sorted list)",
    "after_ab": "Which NFA states are active after 'ab'? (sorted list)",
    "accepts_bbaa": "Does the NFA accept 'bbaa'? (bool)",
    "accepts_baab": "Does the NFA accept 'baab'? (bool)",
    "dfa_states": "How many reachable states does to_dfa() produce? (int)",
    "minimal_states": "How many states remain after minimization? (int)",
    "merged_states": "Which converted DFA states merge? (sorted list)",
}


def containing_ab() -> StateMachine:
    """Recognize exactly the words over {a, b} containing 'ab'."""
    return StateMachine(
        {
            "S0": {"a": ["S0", "S1"], "b": "S0", "start": True, "accept": False},
            "S1": {"b": "S2", "start": False, "accept": False},
            "S2": {"a": "S2", "b": "S2", "start": False, "accept": True},
        }
    )


def observed_answers() -> dict[str, Any]:
    """Compute observations and check them against the language definition."""
    nfa = containing_ab()
    dfa = nfa.to_dfa()
    minimal = nfa.to_dfa().minimize()
    for length in range(7):
        for symbols in product("ab", repeat=length):
            word = "".join(symbols)
            expected = "ab" in word
            if (
                not nfa.accepts(word)
                == dfa.accepts(word)
                == minimal.accepts(word)
                == expected
            ):
                raise AssertionError(f"Language mismatch for {word!r}")
    groups = dfa.minimization_trace()["rounds"][-1]["partitions"]
    return {
        "empty_word": nfa.accepts(""),
        "after_a": nfa.trace("a")[-1]["states"],
        "after_ab": nfa.trace("ab")[-1]["states"],
        "accepts_bbaa": nfa.accepts("bbaa"),
        "accepts_baab": nfa.accepts("baab"),
        "dfa_states": len(dfa.fsa),
        "minimal_states": len(minimal.fsa),
        "merged_states": next(group for group in groups if len(group) > 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check", action="store_true", help="check your edited PREDICTIONS"
    )
    mode.add_argument("--answers", action="store_true", help="show verified answers")
    options = parser.parse_args()
    if not (options.check or options.answers):
        for name, question in QUESTIONS.items():
            print(f"{name}: {question}")
        print("Edit PREDICTIONS in this file, then run with --check.")
        return
    answers = observed_answers()
    failures = 0
    for name, question in QUESTIONS.items():
        if options.answers:
            print(f"{question}\n  {answers[name]!r}")
        elif PREDICTIONS[name] is None:
            print(f"UNANSWERED {name}: {question}")
            failures += 1
        elif (
            type(PREDICTIONS[name]) is type(answers[name])
            and PREDICTIONS[name] == answers[name]
        ):
            print(f"PASS {name}")
        else:
            print(
                f"RETRY {name}: compare your prediction with trace() or minimization_trace()."
            )
            failures += 1
    if failures:
        raise SystemExit(1)
    print(
        "All observations checked; language equivalence verified for 127 short words."
    )


if __name__ == "__main__":
    main()
