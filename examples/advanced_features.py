#!/usr/bin/env python3
"""
Advanced features demonstration for the Python FSA library.

This script shows advanced features including NFA operations, state combination,
arrow minimization, and error handling.
"""

from python_fsa import StateMachine
from python_fsa.exceptions import (
    InvalidFSADefinitionError,
    InvalidStateError,
    InvalidTransitionError,
)


def demonstrate_nfa_operations() -> None:
    """Demonstrate NFA (Non-deterministic Finite Automaton) operations."""
    print("=== NFA Operations ===")

    # Create an NFA that accepts strings containing 'ab' or 'ba'
    nfa = StateMachine(
        {
            "S0": {
                "a": ["S0", "S1"],
                "b": ["S0", "S2"],
                "start": True,
                "accept": False,
            },
            "S1": {"b": "S3", "start": False, "accept": False},
            "S2": {"a": "S3", "start": False, "accept": False},
            "S3": {"a": "S3", "b": "S3", "start": False, "accept": True},
        }
    )

    print("NFA that accepts strings containing 'ab' or 'ba':")
    print(nfa)
    print()

    # Test some strings
    test_strings = ["ab", "ba", "aab", "bba", "abc", "xyz", "abab"]
    for test_str in test_strings:
        try:
            nfa_copy = StateMachine(
                {
                    "S0": {
                        "a": ["S0", "S1"],
                        "b": ["S0", "S2"],
                        "start": True,
                        "accept": False,
                    },
                    "S1": {"b": "S3", "start": False, "accept": False},
                    "S2": {"a": "S3", "start": False, "accept": False},
                    "S3": {"a": "S3", "b": "S3", "start": False, "accept": True},
                }
            )
            result = nfa_copy(*list(test_str))
            print(f"'{test_str}': {'ACCEPTED' if result.accept else 'REJECTED'}")
        except Exception as e:
            print(f"'{test_str}': ERROR - {e}")
    print()


def demonstrate_state_combination() -> None:
    """Demonstrate NFA state combination for DFA conversion."""
    print("=== State Combination ===")

    # Create an NFA
    nfa = StateMachine(
        {
            "S0": {"0": "S0", "1": ["S0", "S1"], "start": True, "accept": False},
            "S1": {"0": "S1", "1": "S1", "start": False, "accept": True},
        }
    )

    print("Original NFA:")
    print(nfa)
    print()

    # Combine states S0 and S1
    combined_state = nfa.combine_states("S0", "S1")
    print("Combined state {S0,S1}:")
    for state_name, state_def in combined_state.items():
        print(f"{state_name}: {state_def}")
    print()


def demonstrate_arrow_minimization() -> None:
    """Demonstrate transition label optimization."""
    print("=== Arrow Minimization ===")

    # Create an FSA with many individual transitions
    fsa = StateMachine.create_divisibility_checker(10, 2)

    print("Original FSA (showing S0 transitions):")
    s0_transitions = fsa.fsa["S0"]
    for symbol, target in s0_transitions.items():
        if symbol not in ("start", "accept"):
            print(f"  {symbol} -> {target}")
    print()

    # Optimize the arrows
    optimized = fsa.minimize_arrows()
    print("Optimized FSA (showing S0 transitions):")
    s0_optimized = optimized["S0"]
    for symbol, target in s0_optimized.items():
        if symbol not in ("start", "accept"):
            print(f"  {symbol} -> {target}")
    print()


def demonstrate_error_handling() -> None:
    """Demonstrate comprehensive error handling."""
    print("=== Error Handling ===")

    # Test invalid FSA definitions
    print("1. Testing invalid FSA definitions:")

    try:
        StateMachine({})  # Empty FSA
    except InvalidFSADefinitionError as e:
        print(f"   Empty FSA: {e}")

    try:
        StateMachine(
            {
                "S0": {"0": "S0", "1": "S1", "start": True, "accept": True},
                "S1": {
                    "0": "S1",
                    "1": "S0",
                    "start": True,
                    "accept": False,
                },  # Multiple start states
            }
        )
    except InvalidFSADefinitionError as e:
        print(f"   Multiple start states: {e}")

    try:
        StateMachine(
            {
                "S0": {
                    "0": "S0",
                    "1": "S2",
                    "start": True,
                    "accept": True,
                },  # S2 doesn't exist
                "S1": {"0": "S1", "1": "S0", "start": False, "accept": False},
            }
        )
    except InvalidStateError as e:
        print(f"   Invalid state reference: {e}")

    print()

    # Test invalid transitions
    print("2. Testing invalid transitions:")
    fsa = StateMachine.create_divisibility_checker(2, 3)

    try:
        fsa(2)  # Invalid symbol for binary FSA
    except InvalidTransitionError as e:
        print(f"   Invalid input symbol: {e}")

    print()


def demonstrate_performance_features() -> None:
    """Demonstrate performance-related features."""
    print("=== Performance Features ===")

    # Test with larger FSAs
    print("1. Creating larger divisibility checkers:")

    for base, divisor in [(2, 7), (3, 5), (10, 11)]:
        fsa = StateMachine.create_divisibility_checker(base, divisor)
        print(f"   Base {base}, divisor {divisor}: {len(fsa.fsa)} states")

    print()

    # Test minimization performance
    print("2. Minimization performance:")

    # Create a DFA that benefits from minimization
    large_fsa = StateMachine(
        {
            "S0": {"0": "S1", "1": "S2", "start": True, "accept": False},
            "S1": {"0": "S0", "1": "S3", "start": False, "accept": False},
            "S2": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S3": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S4": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S5": {"0": "S5", "1": "S5", "start": False, "accept": False},
            "S6": {
                "0": "S4",
                "1": "S5",
                "start": False,
                "accept": True,
            },  # Equivalent to S3
            "S7": {
                "0": "S5",
                "1": "S5",
                "start": False,
                "accept": False,
            },  # Equivalent to S5
        }
    )

    print(f"   Before minimization: {len(large_fsa.fsa)} states")
    minimized = large_fsa.minimize()
    print(f"   After minimization: {len(minimized.fsa)} states")
    print(f"   Reduction: {len(large_fsa.fsa) - len(minimized.fsa)} states")
    print()


def main() -> None:
    """Run all advanced feature demonstrations."""
    print("=== Python FSA Library - Advanced Features ===\n")

    demonstrate_nfa_operations()
    demonstrate_state_combination()
    demonstrate_arrow_minimization()
    demonstrate_error_handling()
    demonstrate_performance_features()

    print("=== Advanced features demonstration completed ===")


if __name__ == "__main__":
    main()
