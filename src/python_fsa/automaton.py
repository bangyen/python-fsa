"""
Finite State Automaton implementation with comprehensive type safety.

This module provides a robust implementation of finite state automata
supporting both deterministic (DFA) and non-deterministic (NFA) automata.
The StateMachine class offers a clean interface for FSA operations including
minimization, state combination, visualization, and input processing.
"""

from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any

from graphviz import Digraph

from .exceptions import (
    InvalidFSADefinitionError,
    InvalidStateError,
    InvalidTransitionError,
    MinimizationError,
)

# Type aliases for better readability
StateName = str
InputSymbol = int | str
TransitionMap = dict[str, StateName | list[StateName]]
StateDefinition = dict[str, Any]
FSADefinition = dict[StateName, StateDefinition]


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

        self.state: str | frozenset[str] = start_states[0]
        self.accept: bool = bool(self.fsa[start_states[0]].get("accept", False))
        self.is_min = False

        # Normalize the FSA to ensure consistent state naming
        self._normalize()
        self.reset()

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
            if not isinstance(state_name, str):
                raise InvalidFSADefinitionError("State names must be strings")
            if not isinstance(state_def, dict):
                raise InvalidFSADefinitionError(
                    f"State '{state_name}' definition must be a dictionary"
                )

            # Validate required fields
            if "start" not in state_def or "accept" not in state_def:
                raise InvalidFSADefinitionError(
                    f"State '{state_name}' must have 'start' and 'accept' fields"
                )

            if not all(isinstance(state_def[key], bool) for key in ("start", "accept")):
                raise InvalidFSADefinitionError(
                    "Start and accept flags must be booleans"
                )

            symbols = [
                str(symbol) for symbol in state_def if symbol not in ("start", "accept")
            ]
            if len(symbols) != len(set(symbols)):
                raise InvalidFSADefinitionError(
                    "Input symbols collide after conversion to strings"
                )

            # Validate transitions reference existing states
            for symbol, target in state_def.items():
                if symbol in ("start", "accept"):
                    continue

                if not isinstance(symbol, (str, int)):
                    raise InvalidFSADefinitionError(
                        "Input symbols must be strings or integers"
                    )
                targets = target if isinstance(target, list) else [target]
                if not all(isinstance(item, str) for item in targets):
                    raise InvalidFSADefinitionError(
                        "Transition targets must be state names"
                    )
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

        # Commit each symbol together with its acceptance status.
        for symbol in inputs:
            if symbol in ("start", "accept"):
                raise InvalidTransitionError(str(self.state), str(symbol))
            destinations: set[str] = set()
            for state in self.active_states:
                definition = self.fsa[state]
                key = symbol if symbol in definition else str(symbol)
                if key not in definition:
                    if self.is_deterministic:
                        raise InvalidTransitionError(
                            state, str(symbol), "No transition defined for this input"
                        )
                    continue
                target = definition[key]
                destinations.update(target if isinstance(target, list) else [target])
            self._set_active(destinations)
        return self

    @property
    def is_deterministic(self) -> bool:
        """Whether every transition has exactly one destination."""
        return not any(
            isinstance(target, list)
            for definition in self.fsa.values()
            for symbol, target in definition.items()
            if symbol not in ("start", "accept")
        )

    def _set_active(self, states: set[str]) -> None:
        self.active_states = frozenset(states)
        self.state = next(iter(states)) if len(states) == 1 else self.active_states
        self.accept = any(self.fsa[state]["accept"] for state in states)

    def reset(self) -> StateMachine:
        """Restart execution at the declared start state."""
        self._set_active(
            {state for state, definition in self.fsa.items() if definition["start"]}
        )
        return self

    def accepts(self, sequence: list[InputSymbol] | str) -> bool:
        """Check a word from the start without changing this machine."""
        machine = StateMachine(deepcopy(self.fsa))
        try:
            return machine(*sequence).accept
        except InvalidTransitionError:
            return False

    def trace(self, sequence: list[InputSymbol] | str) -> list[dict[str, Any]]:
        """Return the initial configuration and each input step without mutation."""
        machine = StateMachine(deepcopy(self.fsa))
        steps: list[dict[str, Any]] = [
            {
                "symbol": None,
                "states": sorted(machine.active_states),
                "accept": machine.accept,
            }
        ]
        for symbol in sequence:
            machine(symbol)
            steps.append(
                {
                    "symbol": symbol,
                    "states": sorted(machine.active_states),
                    "accept": machine.accept,
                }
            )
        return steps

    def to_dfa(self) -> StateMachine:
        """Construct an equivalent complete DFA using reachable state subsets.

        Missing transitions enter the empty subset (a rejecting sink).
        Epsilon transitions are not supported.
        """
        alphabet = sorted(
            {
                symbol
                for definition in self.fsa.values()
                for symbol in definition
                if symbol not in ("start", "accept")
            },
            key=self._symbol_sort_key,
        )
        start = frozenset(
            state for state, definition in self.fsa.items() if definition["start"]
        )
        names = {start: "S0"}
        queue = deque([start])
        result: FSADefinition = {}
        while queue:
            subset = queue.popleft()
            definition: StateDefinition = {
                "start": subset == start,
                "accept": any(self.fsa[state]["accept"] for state in subset),
            }
            for symbol in alphabet:
                targets: set[str] = set()
                for state in subset:
                    target = self.fsa[state].get(symbol, [])
                    targets.update(target if isinstance(target, list) else [target])
                destination = frozenset(targets)
                if destination not in names:
                    names[destination] = f"S{len(names)}"
                    queue.append(destination)
                definition[symbol] = names[destination]
            result[names[subset]] = definition
        return StateMachine(result)

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
        if not state_names:
            raise InvalidFSADefinitionError("At least one state is required")
        # Validate that all states exist
        for state_name in state_names:
            if state_name not in self.fsa:
                raise InvalidStateError(state_name)

        # Create combined state name
        sorted_names = sorted(state_names)
        combined_name = "{" + ",".join(sorted_names) + "}"

        # Collect all possible input symbols
        all_symbols: set[str] = set()
        for state_name in state_names:
            for symbol in self.fsa[state_name]:
                if symbol not in ("start", "accept"):
                    all_symbols.add(symbol)

        # Create combined state definition
        combined_state: StateDefinition = {}

        for symbol in sorted(all_symbols, key=self._symbol_sort_key):
            target_states: set[StateName] = set()
            # Try both the original symbol and string version for key access
            symbol_key = symbol

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
            new_state_def = {
                str(symbol): deepcopy(target) for symbol, target in state_def.items()
            }

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
            if hasattr(self, "active_states"):
                self._set_active({name_mapping[state] for state in self.active_states})
            else:
                assert isinstance(self.state, str)
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
            symbol_groups: dict[Any, list[InputSymbol]] = {}

            for symbol, target in transitions.items():
                if symbol in ("start", "accept"):
                    continue

                target = (
                    tuple(sorted(set(target))) if isinstance(target, list) else target
                )
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

                optimized_transitions[label] = (
                    list(target) if isinstance(target, tuple) else target
                )

            # Preserve start and accept flags
            optimized_transitions["start"] = transitions.get("start", False)
            optimized_transitions["accept"] = transitions.get("accept", False)

            optimized_fsa[state_name] = optimized_transitions

        return optimized_fsa

    def _symbol_sort_key(self, symbol: InputSymbol) -> tuple[int, int | str]:
        """
        Create a sort key for input symbols.

        Args:
            symbol: The input symbol to create a sort key for.

        Returns:
            A sortable key for the symbol.
        """
        if isinstance(symbol, int):
            return (0, symbol)
        return (1, str(symbol))

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
        queue = deque(
            state for state, definition in self.fsa.items() if definition["start"]
        )

        while queue:
            current_state = queue.popleft()
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

    def _minimization_analysis(
        self, collect_trace: bool = False
    ) -> tuple[StateMachine, list[set[str]], list[dict[str, Any]]]:
        """Refine reachable, completed DFA partitions in deterministic order."""
        if not self.is_deterministic:
            raise MinimizationError("Convert an NFA with to_dfa() before minimization")
        machine = self.to_dfa()
        alphabet = [
            symbol for symbol in machine.fsa["S0"] if symbol not in ("start", "accept")
        ]
        accepting = {
            state for state, definition in machine.fsa.items() if definition["accept"]
        }
        partitions = [
            group for group in (accepting, set(machine.fsa) - accepting) if group
        ]
        rounds: list[dict[str, Any]] = []
        while True:
            membership = {
                state: index
                for index, group in enumerate(partitions)
                for state in group
            }
            signatures = {
                state: [membership[machine.fsa[state][symbol]] for symbol in alphabet]
                for state in sorted(machine.fsa)
            }
            refined: list[set[str]] = []
            for group in partitions:
                buckets: dict[tuple[int, ...], set[str]] = {}
                for state in sorted(group):
                    signature = tuple(signatures[state])
                    buckets.setdefault(signature, set()).add(state)
                refined.extend(buckets.values())
            stable = len(refined) == len(partitions)
            if collect_trace:
                rounds.append(
                    {
                        "partitions": [sorted(group) for group in partitions],
                        "signatures": signatures,
                        "stable": stable,
                    }
                )
            if stable:
                break
            partitions = refined
        return machine, partitions, rounds

    def minimization_trace(self) -> dict[str, Any]:
        """Explain DFA partition refinement without changing execution or structure.

        ``definition`` is the reachable, completed DFA used for analysis; its
        names may differ from the original. Each round includes partitions and
        transition signatures: target partition indices in ``alphabet`` order.
        States in the same partition split when their signatures differ.
        The final round has ``stable=True`` and contains the equivalence classes.
        """
        machine, _, rounds = self._minimization_analysis(collect_trace=True)
        return {
            "definition": deepcopy(machine.fsa),
            "alphabet": [
                symbol
                for symbol in machine.fsa["S0"]
                if symbol not in ("start", "accept")
            ],
            "rounds": rounds,
        }

    def minimize(self) -> StateMachine:
        """Minimize a DFA by partition refinement and reset execution.

        Partial DFAs are completed with a rejecting sink before refinement.
        Convert NFAs with ``to_dfa()`` first. Work is computed on a copy so
        failures do not leave the original machine partially modified.
        """
        if self.is_min:
            return self
        machine, partitions, _ = self._minimization_analysis()
        alphabet = [
            symbol for symbol in machine.fsa["S0"] if symbol not in ("start", "accept")
        ]
        accepting = {
            state for state, definition in machine.fsa.items() if definition["accept"]
        }
        partitions.sort(key=lambda group: min(int(state[1:]) for state in group))
        mapping = {
            state: f"S{index}"
            for index, group in enumerate(partitions)
            for state in group
        }
        result: FSADefinition = {}
        for index, group in enumerate(partitions):
            representative = min(group)
            result[f"S{index}"] = {
                **{
                    symbol: mapping[machine.fsa[representative][symbol]]
                    for symbol in alphabet
                },
                "start": "S0" in group,
                "accept": representative in accepting,
            }
        self.fsa = result
        self.reset()
        self.is_min = True
        return self

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
                    for destination in target if isinstance(target, list) else [target]:
                        graph.edge(
                            state_name, destination, label=str(symbol), arrowsize="0.75"
                        )

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
