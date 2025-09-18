"""
Finite State Automaton implementation with comprehensive type safety.

This module provides a robust implementation of finite state automata
supporting both deterministic (DFA) and non-deterministic (NFA) automata.
The StateMachine class offers a clean interface for FSA operations including
minimization, state combination, visualization, and input processing.
"""

from __future__ import annotations

from typing import Any, Dict, List, Union

from graphviz import Digraph

from .exceptions import (
    FSAError,
    InvalidFSADefinitionError,
    InvalidStateError,
    InvalidTransitionError,
    MinimizationError,
)

# Type aliases for better readability
StateName = str
InputSymbol = Union[int, str]
TransitionMap = Dict[
    str, Union[StateName, List[StateName]]
]  # Use str keys for consistency
StateDefinition = Dict[str, Any]
FSADefinition = Dict[StateName, StateDefinition]


class StateMachine:
    """
    A finite state automaton supporting both DFA and NFA operations.

    This class provides a comprehensive interface for working with finite
    state automata, including construction, minimization, state combination,
    visualization, and input processing. It supports both deterministic
    and non-deterministic automata with proper validation and error handling.

    The automaton can be constructed from a dictionary definition or using
    the static factory methods for common patterns like divisibility checkers.
    """

    def __init__(self, fsa: FSADefinition) -> None:
        """
        Initialize the StateMachine with an FSA definition.

        The FSA definition should be a dictionary where each key is a state name
        and each value contains the state's transitions, start status, and accept status.

        Args:
            fsa: Dictionary representation of the FSA with states as keys.

        Raises:
            InvalidFSADefinitionError: If the FSA definition is invalid.
            InvalidStateError: If no start state is found or multiple start states exist.
        """
        self._validate_fsa_definition(fsa)
        self.fsa = fsa.copy()

        # Find and validate the start state
        start_states = [key for key in fsa if fsa[key].get("start", False)]
        if len(start_states) != 1:
            raise InvalidFSADefinitionError(
                f"FSA must have exactly one start state, found {len(start_states)}"
            )

        self.state = start_states[0]
        self.accept = self.fsa[self.state].get("accept", False)
        self.is_min = False

        # Normalize the FSA to ensure consistent state naming
        self._normalize()

    def _validate_fsa_definition(self, fsa: FSADefinition) -> None:
        """
        Validate that the FSA definition is well-formed.

        Args:
            fsa: The FSA definition to validate.

        Raises:
            InvalidFSADefinitionError: If the definition is invalid.
        """
        if not isinstance(fsa, dict):
            raise InvalidFSADefinitionError("FSA definition must be a dictionary")

        if not fsa:
            raise InvalidFSADefinitionError("FSA definition cannot be empty")

        for state_name, state_def in fsa.items():
            if not isinstance(state_def, dict):
                raise InvalidFSADefinitionError(
                    f"State '{state_name}' definition must be a dictionary"
                )

            # Validate required fields
            if "start" not in state_def or "accept" not in state_def:
                raise InvalidFSADefinitionError(
                    f"State '{state_name}' must have 'start' and 'accept' fields"
                )

            # Validate transitions reference existing states
            for symbol, target in state_def.items():
                if symbol in ("start", "accept"):
                    continue

                if isinstance(target, list):
                    for target_state in target:
                        if target_state not in fsa:
                            raise InvalidStateError(
                                target_state,
                                f"Transition from '{state_name}' references non-existent state",
                            )
                elif target not in fsa:
                    raise InvalidStateError(
                        target,
                        f"Transition from '{state_name}' references non-existent state",
                    )

    def __call__(self, *args: InputSymbol | list[InputSymbol]) -> StateMachine:
        """
        Process input symbols through the FSA.

        This method allows the FSA to be called like a function, processing
        input symbols and updating the current state and acceptance status.

        Args:
            *args: Input symbols to process. Can be individual symbols or a list.

        Returns:
            Self to allow method chaining.

        Raises:
            InvalidTransitionError: If a transition is not defined for the current state.
        """
        # Flatten arguments - handle both individual symbols and lists
        inputs: list[InputSymbol] = []
        for arg in args:
            if isinstance(arg, list):
                inputs.extend(arg)
            else:
                inputs.append(arg)

        # Process each input symbol
        for symbol in inputs:
            # Try both the original symbol and string version for key access
            if symbol in self.fsa[self.state]:
                symbol_key = symbol
            elif str(symbol) in self.fsa[self.state]:
                symbol_key = str(symbol)
            else:
                raise InvalidTransitionError(
                    self.state, str(symbol), "No transition defined for this input"
                )

            # Use the key that was actually found in the dictionary
            next_state = self.fsa[self.state][symbol_key]  # type: ignore[index]

            # Handle NFA case where multiple states are possible
            if isinstance(next_state, list):
                if len(next_state) != 1:
                    raise FSAError(
                        f"NFA with multiple possible states not supported in callable mode. "
                        f"State '{self.state}' has {len(next_state)} possible transitions for input '{symbol}'"
                    )
                next_state = next_state[0]

            self.state = next_state

        # Update acceptance status
        self.accept = self.fsa[self.state].get("accept", False)
        return self

    def __str__(self) -> str:
        """
        Create a human-readable string representation of the FSA.

        Returns:
            A formatted table showing states and their properties.
        """
        lines = []
        for state_name, state_def in self.fsa.items():
            # Format transitions
            transitions = []
            for key, value in state_def.items():
                if key not in ("start", "accept"):
                    transitions.append(f"{key}: {value}")

            # Format start and accept flags
            start_flag = "True " if state_def.get("start", False) else "False"
            accept_flag = "True " if state_def.get("accept", False) else "False"

            line = f"{state_name}: | {', '.join(transitions)}, start: {start_flag}, accept: {accept_flag} |"
            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def create_divisibility_checker(base: int, divisor: int) -> StateMachine:
        """
        Create a DFA that checks if a number in a given base is divisible by a divisor.

        This factory method creates a specialized DFA for divisibility checking.
        The automaton processes digits from left to right and maintains the remainder
        modulo the divisor, accepting if the final remainder is zero.

        Args:
            base: The number base (e.g., 2 for binary, 10 for decimal).
            divisor: The number to check divisibility against.

        Returns:
            A StateMachine configured for divisibility checking.

        Raises:
            ValueError: If base or divisor are invalid.
        """
        if base < 2:
            raise ValueError(f"Base must be at least 2, got {base}")
        if divisor < 1:
            raise ValueError(f"Divisor must be at least 1, got {divisor}")

        def create_transitions(state: int) -> dict[Any, Any]:
            """Create transition function for a given state."""
            transitions: dict[Any, Any] = {}
            for symbol in range(base):
                next_state = (base * state + symbol) % divisor
                transitions[str(symbol)] = f"S{next_state}"
            return transitions

        # Create FSA definition
        fsa: FSADefinition = {}
        for state in range(divisor):
            state_name = f"S{state}"
            transitions = create_transitions(state)
            transitions.update({"start": state == 0, "accept": state == 0})
            fsa[state_name] = transitions

        return StateMachine(fsa)

    def combine_states(
        self, *state_names: StateName
    ) -> dict[StateName, StateDefinition]:
        """
        Combine multiple NFA states into a single state.

        This method is used for NFA to DFA conversion and state reduction.
        It creates a new state that represents the union of the given states,
        with transitions that include all possible transitions from the original states.

        Args:
            *state_names: Names of states to combine.

        Returns:
            Dictionary containing the new combined state definition.

        Raises:
            InvalidStateError: If any of the specified states don't exist.
        """
        # Validate that all states exist
        for state_name in state_names:
            if state_name not in self.fsa:
                raise InvalidStateError(state_name)

        # Create combined state name
        sorted_names = sorted(state_names)
        combined_name = "{" + ",".join(sorted_names) + "}"

        # Collect all possible input symbols
        all_symbols: set[InputSymbol] = set()
        for state_name in state_names:
            for symbol in self.fsa[state_name]:
                if symbol not in ("start", "accept"):
                    all_symbols.add(symbol)

        # Create combined state definition
        combined_state: StateDefinition = {}

        for symbol in all_symbols:  # type: ignore[assignment]
            target_states: set[StateName] = set()
            # Try both the original symbol and string version for key access
            if symbol in self.fsa[state_names[0]]:
                symbol_key = symbol
            else:
                symbol_key = str(symbol)

            for state_name in state_names:
                if symbol_key in self.fsa[state_name]:
                    target = self.fsa[state_name][symbol_key]
                    if isinstance(target, list):
                        target_states.update(target)
                    else:
                        target_states.add(target)

            # Set the transition result
            if len(target_states) == 1:
                combined_state[symbol_key] = list(target_states)[0]
            else:
                combined_state[symbol_key] = sorted(target_states)

        # Set start and accept flags
        combined_state["start"] = any(
            self.fsa[state_name].get("start", False) for state_name in state_names
        )
        combined_state["accept"] = any(
            self.fsa[state_name].get("accept", False) for state_name in state_names
        )

        return {combined_name: combined_state}

    def _normalize(self) -> StateMachine:
        """
        Normalize the FSA by renaming states to follow S0, S1, S2... convention.

        This method ensures consistent state naming and is called automatically
        during initialization. It preserves the automaton's behavior while
        standardizing the state names.

        Returns:
            Self to allow method chaining.
        """
        # Sort states by their numeric suffix for consistent ordering
        state_list = sorted(
            self.fsa,
            key=lambda key: int(key[1:]) if key[1:].isdigit() else float("inf"),
        )

        # Create mapping from old names to new names
        name_mapping: dict[str, str] = {
            old_name: f"S{i}" for i, old_name in enumerate(state_list)
        }

        # Create new FSA with normalized names
        new_fsa: FSADefinition = {}
        for old_name, state_def in self.fsa.items():
            new_name = name_mapping[old_name]
            new_state_def = state_def.copy()

            # Update transitions to use new state names
            for key, value in new_state_def.items():
                if key not in ("start", "accept"):
                    if isinstance(value, list):
                        new_state_def[key] = [name_mapping[v] for v in value]
                    else:
                        new_state_def[key] = name_mapping[value]

            new_fsa[new_name] = new_state_def

        self.fsa = new_fsa

        # Update current state name
        if hasattr(self, "state"):
            self.state = name_mapping[self.state]

        return self

    def minimize_arrows(self, add_spaces: bool = False) -> FSADefinition:
        """
        Optimize transition labels by combining symbols that lead to the same state.

        This method reduces visual clutter in FSA representations by grouping
        input symbols that have identical transitions. For example, symbols
        0,2,4,6,8 might be combined into "0,2,4,6,8" if they all lead to the same state.

        Args:
            add_spaces: Whether to add spaces after commas in combined labels.

        Returns:
            Optimized FSA definition with combined transition labels.
        """
        optimized_fsa: FSADefinition = {}

        for state_name, state_def in self.fsa.items():
            transitions = state_def.copy()

            # Group symbols by their target states
            symbol_groups: dict[StateName | list[StateName], list[InputSymbol]] = {}

            for symbol, target in transitions.items():
                if symbol in ("start", "accept"):
                    continue

                if target not in symbol_groups:
                    symbol_groups[target] = []
                symbol_groups[target].append(symbol)

            # Create optimized transitions
            optimized_transitions: StateDefinition = {}

            for target, symbols in symbol_groups.items():
                # Sort symbols for consistent output
                sorted_symbols = sorted(symbols, key=self._symbol_sort_key)

                if len(sorted_symbols) == 1:
                    label = str(sorted_symbols[0])
                else:
                    separator = ", " if add_spaces else ","
                    label = separator.join(str(s) for s in sorted_symbols)

                optimized_transitions[label] = target

            # Preserve start and accept flags
            optimized_transitions["start"] = transitions.get("start", False)
            optimized_transitions["accept"] = transitions.get("accept", False)

            optimized_fsa[state_name] = optimized_transitions

        return optimized_fsa

    def _symbol_sort_key(self, symbol: InputSymbol) -> int | str:
        """
        Create a sort key for input symbols.

        Args:
            symbol: The input symbol to create a sort key for.

        Returns:
            A sortable key for the symbol.
        """
        if isinstance(symbol, int):
            return symbol
        return str(symbol)

    def remove_unreachable_states(self) -> StateMachine:
        """
        Remove states that are not reachable from the start state.

        This method performs a reachability analysis and removes any states
        that cannot be reached from the start state, which is useful for
        cleaning up FSAs before minimization.

        Returns:
            Self to allow method chaining.
        """
        # Find all reachable states using BFS
        reachable_states: set[StateName] = set()
        queue = [self.state]

        while queue:
            current_state = queue.pop(0)
            if current_state in reachable_states:
                continue

            reachable_states.add(current_state)

            # Add all states reachable from current state
            for symbol, target in self.fsa[current_state].items():
                if symbol in ("start", "accept"):
                    continue

                if isinstance(target, list):
                    for target_state in target:
                        if target_state not in reachable_states:
                            queue.append(target_state)
                elif target not in reachable_states:
                    queue.append(target)

        # Remove unreachable states
        states_to_remove = set(self.fsa.keys()) - reachable_states
        for state in states_to_remove:
            del self.fsa[state]

        return self

    def minimize(self) -> StateMachine:
        """
        Minimize the DFA using the table-filling algorithm.

        This method implements the standard DFA minimization algorithm that
        identifies and merges equivalent states. The algorithm works by
        iteratively refining partitions of states until no further refinement
        is possible.

        Returns:
            Self to allow method chaining.

        Raises:
            MinimizationError: If minimization fails due to an unexpected condition.
        """
        if self.is_min:
            return self

        try:
            # Remove unreachable states first
            self.remove_unreachable_states()
            self._normalize()

            # Get accepting states
            accepting_states = {
                int(state_name[1:])
                for state_name, state_def in self.fsa.items()
                if state_def.get("accept", False)
            }

            # Initialize table with accepting/non-accepting distinction
            num_states = len(self.fsa)
            table = self._initialize_minimization_table(num_states, accepting_states)

            # Fill the table using the table-filling algorithm
            table = self._fill_minimization_table(table, num_states)

            # Find equivalent state groups
            equivalent_groups = self._find_equivalent_states(table, num_states)

            # Merge equivalent states
            self._merge_equivalent_states(equivalent_groups)

            # Normalize and mark as minimized
            self._normalize()
            self.is_min = True

        except Exception as e:
            raise MinimizationError(f"Minimization failed: {str(e)}") from e

        return self

    def _initialize_minimization_table(
        self, num_states: int, accepting_states: set[int]
    ) -> list[list[int]]:
        """
        Initialize the minimization table with accepting/non-accepting distinction.

        Args:
            num_states: Total number of states in the FSA.
            accepting_states: Set of accepting state indices.

        Returns:
            Initialized table with 1s marking distinguishable state pairs.
        """
        table = [[0 for _ in range(num_states)] for _ in range(num_states)]

        # Mark pairs where one state is accepting and the other is not
        for i in range(num_states):
            for j in range(i):
                if (i in accepting_states) != (j in accepting_states):
                    table[i][j] = table[j][i] = 1

        return table

    def _fill_minimization_table(
        self, table: list[list[int]], num_states: int
    ) -> list[list[int]]:
        """
        Fill the minimization table using the table-filling algorithm.

        Args:
            table: The minimization table to fill.
            num_states: Total number of states in the FSA.

        Returns:
            The filled minimization table.
        """
        changed = True
        while changed:
            changed = False
            old_table = [row[:] for row in table]

            for i in range(num_states):
                for j in range(i):
                    if table[i][j] == 0:  # States not yet marked as distinguishable
                        # Check if they become distinguishable through transitions
                        for symbol in self.fsa[f"S{i}"]:
                            if symbol in ("start", "accept"):
                                continue

                            state_i_target = self.fsa[f"S{i}"][symbol]
                            state_j_target = self.fsa[f"S{j}"][symbol]

                            # Handle both single states and lists
                            if isinstance(state_i_target, list):
                                state_i_target = state_i_target[0]
                            if isinstance(state_j_target, list):
                                state_j_target = state_j_target[0]

                            target_i = int(state_i_target[1:])
                            target_j = int(state_j_target[1:])

                            if old_table[target_i][target_j] == 1:
                                table[i][j] = table[j][i] = 1
                                changed = True
                                break

        return table

    def _find_equivalent_states(
        self, table: list[list[int]], num_states: int
    ) -> list[set[int]]:
        """
        Find groups of equivalent states from the filled table.

        Args:
            table: The filled minimization table.
            num_states: Total number of states in the FSA.

        Returns:
            List of sets containing equivalent state indices.
        """
        equivalent_groups = []
        processed = set()

        for i in range(num_states):
            if i in processed:
                continue

            # Find all states equivalent to state i
            equivalent_set = {i}
            for j in range(i + 1, num_states):
                if table[i][j] == 0:  # States are equivalent
                    equivalent_set.add(j)

            equivalent_groups.append(equivalent_set)
            processed.update(equivalent_set)

        return equivalent_groups

    def _merge_equivalent_states(self, equivalent_groups: list[set[int]]) -> None:
        """
        Merge equivalent states in the FSA.

        Args:
            equivalent_groups: Groups of equivalent state indices to merge.
        """
        # Create mapping from old states to new merged states
        state_mapping: dict[StateName, StateName] = {}

        for group in equivalent_groups:
            if len(group) > 1:  # Only merge groups with multiple states
                sorted_group = sorted(group)
                keep_state = f"S{sorted_group[0]}"

                # Map all states in the group to the kept state
                for state_idx in sorted_group[1:]:
                    state_mapping[f"S{state_idx}"] = keep_state
                    del self.fsa[f"S{state_idx}"]

        # Update all transitions to use the new state names
        for _state_name, state_def in self.fsa.items():
            for symbol, target in state_def.items():
                if symbol in ("start", "accept"):
                    continue

                if isinstance(target, list):
                    state_def[symbol] = [state_mapping.get(t, t) for t in target]
                else:
                    state_def[symbol] = state_mapping.get(target, target)

    def create_graph(
        self,
        optimize_arrows: bool = True,
        add_spaces: bool = False,
        circular_layout: bool = False,
    ) -> Digraph:
        """
        Create a Graphviz visualization of the FSA.

        This method generates a visual representation of the FSA using Graphviz,
        which can be rendered as PNG, SVG, or other formats. The visualization
        shows states as circles (double circles for accepting states) and
        transitions as labeled arrows.

        Args:
            optimize_arrows: Whether to combine transition labels for clarity.
            add_spaces: Whether to add spaces in combined transition labels.
            circular_layout: Whether to use circular layout instead of left-to-right.

        Returns:
            A Graphviz Digraph object representing the FSA.
        """
        # Get FSA definition (optimized if requested)
        fsa_def = self.minimize_arrows(add_spaces) if optimize_arrows else self.fsa

        # Create the graph
        graph = Digraph()

        # Set graph attributes
        if circular_layout:
            graph.attr(rankdir="LR", size="8,5", layout="circo")
        else:
            graph.attr(rankdir="LR", size="8,5")

        # Add invisible start node
        graph.node("", shape="none", height="0", width="0")

        # Add states
        for state_name, state_def in fsa_def.items():
            if state_def.get("accept", False):
                graph.node(state_name, shape="doublecircle")
            else:
                graph.node(state_name, shape="circle")

            # Add start arrow
            if state_def.get("start", False):
                graph.edge("", state_name, arrowsize="0.75")

            # Add transitions
            for symbol, target in state_def.items():
                if symbol not in ("start", "accept"):
                    graph.edge(state_name, target, label=str(symbol), arrowsize="0.75")

        return graph

    # Legacy method aliases for backward compatibility
    @staticmethod
    def div_by(base: int, num: int) -> StateMachine:
        """Legacy alias for create_divisibility_checker."""
        return StateMachine.create_divisibility_checker(base, num)

    def combine(self, *keys: StateName) -> dict[StateName, StateDefinition]:
        """Legacy alias for combine_states."""
        return self.combine_states(*keys)

    def norm(self) -> StateMachine:
        """Legacy alias for _normalize."""
        return self._normalize()

    def arrow_min(self, space: bool = False) -> FSADefinition:
        """Legacy alias for minimize_arrows."""
        return self.minimize_arrows(space)

    def remove(self) -> StateMachine:
        """Legacy alias for remove_unreachable_states."""
        return self.remove_unreachable_states()

    def fsa_min(self) -> StateMachine:
        """Legacy alias for minimize."""
        return self.minimize()

    def graph(self, space: bool = False, circle: bool = False) -> Digraph:
        """Legacy alias for create_graph."""
        return self.create_graph(
            optimize_arrows=True, add_spaces=space, circular_layout=circle
        )
