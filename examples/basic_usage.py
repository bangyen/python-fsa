#!/usr/bin/env python3
"""
Basic usage examples for the Python FSA library.

This script demonstrates the core functionality of the finite state automaton
library including creation, input processing, minimization, and visualization.
"""

from python_fsa import StateMachine


def main() -> None:
    """Demonstrate basic FSA operations."""
    print("=== Python FSA Library - Basic Usage Examples ===\n")

    # Example 1: Create a divisibility checker
    print("1. Creating a binary divisibility-by-3 checker:")
    fsa = StateMachine.create_divisibility_checker(2, 3)
    print(f"   Initial state: {fsa.state}")
    print(f"   Is accepting: {fsa.accept}")
    print()

    # Example 2: Process some inputs
    print("2. Processing binary inputs:")
    test_cases = [
        ([1, 1], "Binary 11 (decimal 3)"),
        ([1, 0, 1], "Binary 101 (decimal 5)"),
        ([1, 1, 0], "Binary 110 (decimal 6)"),
        ([0], "Binary 0 (decimal 0)"),
    ]

    for input_seq, description in test_cases:
        fsa_copy = StateMachine.create_divisibility_checker(2, 3)
        result = fsa_copy(*input_seq)
        print(f"   {description}: {'ACCEPTED' if result.accept else 'REJECTED'}")
    print()

    # Example 3: Show the FSA structure
    print("3. FSA Structure:")
    print(fsa)
    print()

    # Example 4: Create a custom FSA
    print("4. Creating a custom FSA (accepts strings ending in 'ab'):")

    test_strings = ["ab", "aab", "baab", "abab", "ba", "a"]
    for test_str in test_strings:
        # Create a fresh copy for each test to avoid state pollution
        fsa_copy = StateMachine(
            {
                "S0": {"a": "S1", "b": "S0", "start": True, "accept": False},
                "S1": {"a": "S1", "b": "S2", "start": False, "accept": False},
                "S2": {"a": "S1", "b": "S0", "start": False, "accept": True},
            }
        )
        result = fsa_copy(*list(test_str))
        print(f"   '{test_str}': {'ACCEPTED' if result.accept else 'REJECTED'}")
    print()

    # Example 5: Minimization
    print("5. DFA Minimization example:")
    # Create a DFA that can be minimized
    minimizable_fsa = StateMachine(
        {
            "S0": {"0": "S1", "1": "S2", "start": True, "accept": False},
            "S1": {"0": "S0", "1": "S3", "start": False, "accept": False},
            "S2": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S3": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S4": {"0": "S4", "1": "S5", "start": False, "accept": True},
            "S5": {"0": "S5", "1": "S5", "start": False, "accept": False},
        }
    )

    print("   Before minimization:")
    print(f"   Number of states: {len(minimizable_fsa.fsa)}")

    minimized_fsa = minimizable_fsa.minimize()
    print("   After minimization:")
    print(f"   Number of states: {len(minimized_fsa.fsa)}")
    print("   Minimized FSA:")
    print(minimized_fsa)
    print()

    # Example 6: Graph visualization
    print("6. Graph visualization:")
    try:
        graph = fsa.create_graph()
        print("   Graph created successfully!")
        print("   To render: graph.render('divisibility_by_3', format='png')")
        print("   (Requires Graphviz to be installed)")
        # Use the graph variable to avoid unused variable warning
        print(f"   Graph has {len(graph.body)} elements")
    except Exception as e:
        print(f"   Graph creation failed: {e}")
        print("   Make sure Graphviz is installed: sudo apt-get install graphviz")
    print()

    print("=== Examples completed ===")


if __name__ == "__main__":
    main()
