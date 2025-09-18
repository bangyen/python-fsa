"""
Comprehensive test suite for the Python FSA library.

This module contains tests for all major functionality including
DFA/NFA operations, minimization, state combination, visualization,
and error handling.
"""

import math
from typing import Any

import pytest
from python_fsa import StateMachine
from python_fsa.exceptions import (
    InvalidFSADefinitionError,
    InvalidStateError,
    InvalidTransitionError,
)


class TestStateMachine:
    """Test cases for the StateMachine class."""

    def test_divisibility_checker_creation(self) -> None:
        """Test creation of divisibility checker FSAs."""
        for base in range(2, 5):
            for num in range(2, 5):
                fsa = StateMachine.create_divisibility_checker(base, num)
                assert (
                    fsa.state == "S0"
                ), f"Divisibility FSAs should start at S0 for base {base}, divisor {num}"

    def test_divisibility_checker_validation(self) -> None:
        """Test input validation for divisibility checker creation."""
        with pytest.raises(ValueError, match="Base must be at least 2"):
            StateMachine.create_divisibility_checker(1, 3)

        with pytest.raises(ValueError, match="Divisor must be at least 1"):
            StateMachine.create_divisibility_checker(2, 0)

    def test_basic_input_processing(self) -> None:
        """Test basic input processing through the FSA."""
        fsa = StateMachine.create_divisibility_checker(2, 3)

        # Test multiple arguments
        assert fsa(1, 1).accept, "Multiple args: 3 mod 3 (base 2)"

        # Test with leading zero
        fsa = StateMachine.create_divisibility_checker(2, 3)
        assert fsa(0, 1, 1).accept, "Leading zero: 3 mod 3 (base 2)"

        # Test with list input
        fsa = StateMachine.create_divisibility_checker(2, 3)
        assert fsa([1, 1]).accept, "List: 3 mod 3 (base 2)"

        # Test method chaining
        fsa = StateMachine.create_divisibility_checker(2, 3)
        assert fsa(1)(1).accept, "Multiple calls: 3 mod 3 (base 2)"

    def test_minimized_fsa_processing(self) -> None:
        """Test input processing on minimized FSAs."""
        fsa = StateMachine.create_divisibility_checker(2, 8).minimize()

        # Test various input patterns
        assert not fsa(1, 1, 1, 0).accept, "Multiple args: 14 mod 8 (base 2)"
        assert not fsa(0, 1, 1, 1, 0).accept, "Leading zero: 14 mod 8 (base 2)"
        assert not fsa([1, 1, 1, 0]).accept, "List: 14 mod 8 (base 2)"
        assert not fsa(1)(1)(1)(0).accept, "Multiple calls: 14 mod 8 (base 2)"

    def test_wikipedia_minimization_example(self) -> None:
        """Test DFA minimization using the Wikipedia example."""
        pre = {
            "S0": {"0": "S1", "1": "S2", "start": True, "accept": False},
            "S1": {"0": "S0", "1": "S3", "start": False, "accept": False},
            "S2": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S3": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S4": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S5": {"0": "S5", "1": "S5", "start": False, "accept": False},
        }
        expected_post = {
            "S0": {"0": "S0", "1": "S1", "start": True, "accept": False},
            "S1": {"0": "S1", "1": "S2", "start": False, "accept": True},
            "S2": {"0": "S2", "1": "S2", "start": False, "accept": False},
        }

        fsa = StateMachine(pre).minimize()
        assert fsa.fsa == expected_post, "DFA Minimization (Wikipedia Example)"
        assert not fsa.accept, "S0 is not an accept state"
        assert fsa(1)(0).accept, "Multiple calls, S4 (new S1) is an accept state"
        assert (
            fsa.minimize() is fsa
        ), "Multiple minimization calls should return same object"

    def test_malta_minimization_example(self) -> None:
        """Test DFA minimization using the Malta example."""
        pre = {
            "S0": {"a": "S1", "b": "S0", "start": True, "accept": True},
            "S1": {"a": "S0", "b": "S2", "start": False, "accept": True},
            "S2": {"a": "S2", "b": "S1", "start": False, "accept": False},
            "S3": {"a": "S1", "b": "S2", "start": False, "accept": False},
        }
        expected_post = {
            "S0": {"a": "S1", "b": "S0", "start": True, "accept": True},
            "S1": {"a": "S0", "b": "S2", "start": False, "accept": True},
            "S2": {"a": "S2", "b": "S1", "start": False, "accept": False},
        }

        fsa = StateMachine(pre).minimize()
        assert fsa.fsa == expected_post, "DFA Minimization (Malta Example)"
        assert fsa.accept, "S0 is an accept state"
        assert not fsa("a")("b").accept, "Multiple calls, S2 is not an accept state"
        assert (
            fsa.minimize() is fsa
        ), "Multiple minimization calls should return same object"

    def test_state_combination(self) -> None:
        """Test NFA state combination functionality."""
        test_fsa = {
            "S0": {"0": "S0", "1": "S1", "start": True, "accept": False},
            "S1": {"0": "S1", "1": "S2", "start": False, "accept": True},
            "S2": {"0": "S2", "1": "S2", "start": False, "accept": False},
        }
        expected_combination = {
            "{S1,S2}": {"0": ["S1", "S2"], "1": "S2", "start": False, "accept": True}
        }

        fsa = StateMachine(test_fsa)
        result = fsa.combine_states("S1", "S2")
        assert result == expected_combination, "State combination test"

    def test_string_representation(self) -> None:
        """Test string representation of FSAs."""
        fsa = StateMachine.create_divisibility_checker(2, 3)
        str_repr = str(fsa)

        # Check that all states are represented
        assert "S0:" in str_repr
        assert "S1:" in str_repr
        assert "S2:" in str_repr

        # Check that transitions are shown
        assert "0:" in str_repr
        assert "1:" in str_repr

        # Check that start and accept flags are shown
        assert "start:" in str_repr
        assert "accept:" in str_repr

    def test_graph_creation(self) -> None:
        """Test Graphviz graph creation."""
        fsa = StateMachine.create_divisibility_checker(10, 2)
        graph = fsa.create_graph()

        # Check that graph source contains expected elements
        graph_source = graph.source

        # Basic graph structure
        assert "digraph" in graph_source
        assert "rankdir=LR" in graph_source
        assert 'size="8,5"' in graph_source

        # States
        assert "S0" in graph_source
        assert "S1" in graph_source

        # Transitions with combined labels
        assert "0,2,4,6,8" in graph_source
        assert "1,3,5,7,9" in graph_source

    def test_fsa_definition_validation(self) -> None:
        """Test FSA definition validation."""
        # Test empty definition
        with pytest.raises(
            InvalidFSADefinitionError, match="FSA definition cannot be empty"
        ):
            StateMachine({})

        # Test non-dictionary definition
        with pytest.raises(
            InvalidFSADefinitionError, match="FSA definition must be a dictionary"
        ):
            StateMachine("not a dict")  # type: ignore[arg-type]

        # Test missing start state
        invalid_fsa = {
            "S0": {"0": "S0", "1": "S1", "start": False, "accept": True},
            "S1": {"0": "S1", "1": "S0", "start": False, "accept": False},
        }
        with pytest.raises(
            InvalidFSADefinitionError, match="FSA must have exactly one start state"
        ):
            StateMachine(invalid_fsa)

        # Test multiple start states
        invalid_fsa = {
            "S0": {"0": "S0", "1": "S1", "start": True, "accept": True},
            "S1": {"0": "S1", "1": "S0", "start": True, "accept": False},
        }
        with pytest.raises(
            InvalidFSADefinitionError, match="FSA must have exactly one start state"
        ):
            StateMachine(invalid_fsa)

        # Test missing required fields
        invalid_fsa = {
            "S0": {"0": "S0", "1": "S1", "start": True},  # Missing 'accept'
            "S1": {"0": "S1", "1": "S0", "start": False, "accept": False},
        }
        with pytest.raises(
            InvalidFSADefinitionError, match="must have 'start' and 'accept' fields"
        ):
            StateMachine(invalid_fsa)

        # Test invalid state reference
        invalid_fsa = {
            "S0": {
                "0": "S0",
                "1": "S2",
                "start": True,
                "accept": True,
            },  # S2 doesn't exist
            "S1": {"0": "S1", "1": "S0", "start": False, "accept": False},
        }
        with pytest.raises(InvalidStateError, match="references non-existent state"):
            StateMachine(invalid_fsa)

    def test_invalid_transitions(self) -> None:
        """Test handling of invalid transitions."""
        fsa = StateMachine.create_divisibility_checker(2, 3)

        # Test invalid input symbol
        with pytest.raises(InvalidTransitionError, match="No transition defined"):
            fsa(2)  # Invalid symbol for binary FSA

    def test_legacy_method_aliases(self) -> None:
        """Test that legacy method names still work for backward compatibility."""
        fsa = StateMachine.create_divisibility_checker(2, 3)

        # Test legacy div_by method
        legacy_fsa = StateMachine.div_by(2, 3)
        assert legacy_fsa.fsa == fsa.fsa

        # Test legacy method aliases
        assert fsa.norm() is fsa
        assert fsa.remove() is fsa
        assert fsa.fsa_min() is fsa
        assert fsa.graph() is not None

    def test_arrow_minimization(self) -> None:
        """Test transition label optimization."""
        fsa = StateMachine.create_divisibility_checker(10, 2)
        optimized = fsa.minimize_arrows()

        # Check that labels are combined
        s0_transitions = optimized["S0"]
        assert any("0,2,4,6,8" in str(label) for label in s0_transitions.keys())
        assert any("1,3,5,7,9" in str(label) for label in s0_transitions.keys())

    def test_unreachable_state_removal(self) -> None:
        """Test removal of unreachable states."""
        fsa_with_unreachable = {
            "S0": {"0": "S0", "1": "S1", "start": True, "accept": True},
            "S1": {"0": "S1", "1": "S2", "start": False, "accept": False},
            "S2": {"0": "S2", "1": "S2", "start": False, "accept": False},
            "S3": {
                "0": "S3",
                "1": "S3",
                "start": False,
                "accept": False,
            },  # Unreachable
        }

        fsa = StateMachine(fsa_with_unreachable)
        fsa.remove_unreachable_states()

        # S3 should be removed
        assert "S3" not in fsa.fsa
        assert len(fsa.fsa) == 3

    def test_math_isclose_for_float_tolerances(self) -> None:
        """Test using math.isclose for float comparisons in tests."""
        # This test demonstrates the recommended approach for float comparisons
        result = 0.1 + 0.2
        expected = 0.3

        # Use math.isclose instead of direct equality for floats
        assert math.isclose(
            result, expected, rel_tol=1e-9
        ), "Float comparison should use math.isclose"

    def test_seeded_randomness(self) -> None:
        """Test that randomness is properly seeded for reproducible tests."""
        import random

        # Seed the random number generator for reproducible tests
        random.seed(42)
        first_run = [random.random() for _ in range(5)]

        random.seed(42)
        second_run = [random.random() for _ in range(5)]

        assert first_run == second_run, "Seeded randomness should be reproducible"


# Pytest fixtures for common test data
@pytest.fixture  # type: ignore[misc]
def simple_dfa() -> dict[str, dict[str, Any]]:
    """A simple DFA for testing."""
    return {
        "S0": {"0": "S0", "1": "S1", "start": True, "accept": True},
        "S1": {"0": "S1", "1": "S0", "start": False, "accept": False},
    }


@pytest.fixture  # type: ignore[misc]
def simple_nfa() -> dict[str, dict[str, Any]]:
    """A simple NFA for testing."""
    return {
        "S0": {"0": "S0", "1": ["S0", "S1"], "start": True, "accept": False},
        "S1": {"0": "S1", "1": "S1", "start": False, "accept": True},
    }


def test_fixture_usage(simple_dfa: dict[str, dict[str, Any]]) -> None:
    """Test that fixtures work correctly."""
    fsa = StateMachine(simple_dfa)
    assert fsa.state == "S0"
    assert fsa.accept is True


# Parametrized tests for comprehensive coverage
@pytest.mark.parametrize("base,divisor", [(2, 3), (3, 4), (10, 5)])  # type: ignore[misc]
def test_divisibility_checkers(base: int, divisor: int) -> None:
    """Test divisibility checkers with various bases and divisors."""
    fsa = StateMachine.create_divisibility_checker(base, divisor)

    # Test that it starts in the correct state
    assert fsa.state == "S0"

    # Test that S0 is accepting (divisible by divisor)
    assert fsa.accept is True

    # Test with zero input
    fsa_zero = StateMachine.create_divisibility_checker(base, divisor)
    assert fsa_zero(0).accept is True


@pytest.mark.parametrize(
    "input_sequence,expected",
    [
        ([1, 1], True),  # 3 in binary, divisible by 3
        ([1, 0, 1], False),  # 5 in binary, not divisible by 3
        ([1, 1, 0], True),  # 6 in binary, divisible by 3
    ],
)  # type: ignore[misc]
def test_binary_divisibility_by_three(
    input_sequence: list[int], expected: bool
) -> None:
    """Test binary divisibility by 3 with specific input sequences."""
    fsa = StateMachine.create_divisibility_checker(2, 3)
    result = fsa(*input_sequence)
    assert result.accept == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
