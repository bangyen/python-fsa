"""Behavioral regressions and language equivalence checks."""

from itertools import product

import pytest

from python_fsa import (
    InvalidFSADefinitionError,
    InvalidTransitionError,
    MinimizationError,
    StateMachine,
)


def ending_in_one() -> StateMachine:
    return StateMachine(
        {
            "S0": {"0": "S0", "1": "S1", "start": True, "accept": False},
            "S1": {"0": "S0", "1": "S1", "start": False, "accept": True},
        }
    )


def test_failed_batch_keeps_acceptance_consistent() -> None:
    machine = ending_in_one()
    with pytest.raises(InvalidTransitionError):
        machine(1, "invalid")
    assert machine.state == "S1"
    assert machine.accept
    assert machine.reset().state == "S0"
    assert not machine.accept


def test_metadata_is_not_an_input_symbol() -> None:
    with pytest.raises(InvalidTransitionError):
        ending_in_one()("start")


def test_minimize_after_processing_preserves_start_and_resets() -> None:
    machine = StateMachine(
        {
            "S0": {"a": "S1", "start": True, "accept": False},
            "S1": {"a": "S1", "start": False, "accept": True},
        }
    )
    machine("a").minimize()
    assert not machine.accept
    assert not machine.accepts("")
    assert machine.accepts("a")
    assert sum(definition["start"] for definition in machine.fsa.values()) == 1


def test_merging_current_and_start_states() -> None:
    machine = StateMachine(
        {
            "S0": {"a": "S1", "start": False, "accept": True},
            "S1": {"a": "S0", "start": True, "accept": True},
        }
    )
    machine("a").minimize()
    assert len(machine.fsa) == 1
    assert machine.fsa["S0"]["start"]
    assert machine.accept


def test_nfa_execution_conversion_and_visualization() -> None:
    nfa = StateMachine(
        {
            "S0": {"a": ["S0", "S1"], "b": "S0", "start": True, "accept": False},
            "S1": {"b": "S2", "start": False, "accept": False},
            "S2": {"a": "S2", "b": "S2", "start": False, "accept": True},
        }
    )
    assert not nfa("a").accept
    assert nfa.active_states == frozenset({"S0", "S1"})
    assert nfa("b").accept
    assert "S0 -> S1" in nfa.create_graph().source
    assert "S0 -> S1" in nfa.create_graph(optimize_arrows=False).source
    dfa = nfa.to_dfa()
    minimized = nfa.to_dfa().minimize()
    for length in range(6):
        for symbols in product("ab", repeat=length):
            word = "".join(symbols)
            assert (
                nfa.accepts(word)
                == dfa.accepts(word)
                == minimized.accepts(word)
                == ("ab" in word)
            )
    original = nfa.fsa.copy()
    with pytest.raises(MinimizationError):
        nfa.minimize()
    assert nfa.fsa == original


def test_empty_nfa_destination_and_missing_transition() -> None:
    machine = StateMachine({"S0": {"a": [], "start": True, "accept": True}})
    assert not machine("a").accept
    assert machine.active_states == frozenset()
    assert not machine("b").accept
    assert not machine.to_dfa().accepts("a")


@pytest.mark.parametrize("base,divisor", [(2, 3), (2, 8), (3, 4), (10, 5)])
def test_minimization_preserves_arithmetic(base: int, divisor: int) -> None:
    original = StateMachine.div_by(base, divisor)
    minimized = StateMachine.div_by(base, divisor).minimize()
    for length in range(4):
        for symbols in product(range(base), repeat=length):
            value = 0
            for digit in symbols:
                value = base * value + digit
            assert (
                original.accepts(list(symbols))
                == minimized.accepts(list(symbols))
                == (value % divisor == 0)
            )


def test_partial_dfa_completion_preserves_language() -> None:
    machine = StateMachine(
        {
            "S0": {"a": "S1", "start": True, "accept": False},
            "S1": {"b": "S1", "start": False, "accept": True},
        }
    )
    minimized = StateMachine(machine.fsa).minimize()
    for length in range(5):
        for symbols in product("ab", repeat=length):
            word = "".join(symbols)
            assert machine.accepts(word) == minimized.accepts(word)


def test_independent_checks_and_teaching_trace() -> None:
    machine = ending_in_one()(1)
    before = (machine.state, machine.active_states, machine.accept)
    assert not machine.accepts("10")
    assert machine.trace("01") == [
        {"symbol": None, "states": ["S0"], "accept": False},
        {"symbol": "0", "states": ["S0"], "accept": False},
        {"symbol": "1", "states": ["S1"], "accept": True},
    ]
    assert (machine.state, machine.active_states, machine.accept) == before


def test_validation_and_mixed_symbol_normalization() -> None:
    with pytest.raises(InvalidFSADefinitionError, match="booleans"):
        StateMachine({"S0": {"start": 1, "accept": False}})
    with pytest.raises(InvalidFSADefinitionError, match="state names"):
        StateMachine({"S0": {"a": {}, "start": True, "accept": False}})
    with pytest.raises(InvalidFSADefinitionError, match="collide"):
        StateMachine({"S0": {1: "S0", "1": "S0", "start": True, "accept": False}})
    machine = StateMachine({"S0": {1: "S0", "a": "S0", "start": True, "accept": False}})
    assert "1,a" in machine.create_graph().source
    with pytest.raises(InvalidFSADefinitionError):
        machine.combine_states()


def test_definition_is_copied() -> None:
    definition = {"S0": {"a": ["S0"], "start": True, "accept": False}}
    machine = StateMachine(definition)
    definition["S0"]["a"].clear()
    assert machine.fsa["S0"]["a"] == ["S0"]
