"""Trace an NFA recognizing words containing 'ab' and compare its conversions."""

from python_fsa import StateMachine


def main() -> None:
    nfa = StateMachine(
        {
            "S0": {"a": ["S0", "S1"], "b": "S0", "start": True, "accept": False},
            "S1": {"b": "S2", "start": False, "accept": False},
            "S2": {"a": "S2", "b": "S2", "start": False, "accept": True},
        }
    )
    word = "baab"
    print(f"Execution trace for {word!r}:")
    for step in nfa.trace(word):
        print(step)
    dfa = nfa.to_dfa()
    minimal = nfa.to_dfa().minimize()
    for name, machine in (("NFA", nfa), ("DFA", dfa), ("minimal DFA", minimal)):
        print(f"{name}: {len(machine.fsa)} states; accepted={machine.accepts(word)}")
        assert machine.accepts(word)
        assert not machine.accepts("bbaa")


if __name__ == "__main__":
    main()
