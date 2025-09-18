"""
Python FSA - A comprehensive finite state automaton library.

This package provides a complete implementation of finite state automata
including deterministic (DFA) and non-deterministic (NFA) automata with
operations for minimization, combination, visualization, and more.

The main class StateMachine provides a clean interface for working with
FSAs, while supporting both dictionary-based and programmatic construction.
"""

from .automaton import StateMachine
from .exceptions import FSAError, InvalidStateError, InvalidTransitionError

__version__ = "1.0.0"
__all__ = ["StateMachine", "FSAError", "InvalidStateError", "InvalidTransitionError"]
