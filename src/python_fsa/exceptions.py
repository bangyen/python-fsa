"""
Custom exceptions for the Python FSA library.

These exceptions provide clear, meaningful error messages for common
FSA operations and validation failures.
"""


class FSAError(Exception):
    """Base exception for all FSA-related errors."""

    def __init__(self, message: str) -> None:
        """Initialize the FSA error with a descriptive message.

        Args:
            message: A clear description of what went wrong.
        """
        super().__init__(message)
        self.message = message


class InvalidStateError(FSAError):
    """Raised when an invalid state is referenced in FSA operations.

    This exception is used when trying to access states that don't exist
    or when state names don't follow the expected format.
    """

    def __init__(self, state: str, message: str = "") -> None:
        """Initialize with the invalid state name.

        Args:
            state: The state name that caused the error.
            message: Optional additional context about the error.
        """
        if not message:
            message = f"Invalid state '{state}' referenced in FSA"
        super().__init__(message)
        self.state = state


class InvalidTransitionError(FSAError):
    """Raised when an invalid transition is attempted.

    This exception is used when trying to make transitions with invalid
    input symbols or when transitions lead to non-existent states.
    """

    def __init__(self, from_state: str, input_symbol: str, message: str = "") -> None:
        """Initialize with transition details.

        Args:
            from_state: The state where the transition was attempted.
            input_symbol: The input symbol that caused the error.
            message: Optional additional context about the error.
        """
        if not message:
            message = (
                f"Invalid transition from '{from_state}' on input '{input_symbol}'"
            )
        super().__init__(message)
        self.from_state = from_state
        self.input_symbol = input_symbol


class InvalidFSADefinitionError(FSAError):
    """Raised when the FSA definition is invalid or malformed.

    This exception is used during FSA construction when the provided
    definition doesn't meet the requirements for a valid FSA.
    """

    def __init__(self, message: str) -> None:
        """Initialize with a description of the definition error.

        Args:
            message: A clear description of what's wrong with the FSA definition.
        """
        super().__init__(f"Invalid FSA definition: {message}")


class MinimizationError(FSAError):
    """Raised when FSA minimization fails.

    This exception is used when the minimization algorithm encounters
    an unexpected condition or fails to complete.
    """

    def __init__(self, message: str) -> None:
        """Initialize with a description of the minimization error.

        Args:
            message: A clear description of what went wrong during minimization.
        """
        super().__init__(f"FSA minimization failed: {message}")
