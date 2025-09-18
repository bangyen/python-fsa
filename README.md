# Python FSA - Finite State Automaton Library

[![CI](https://github.com/bangyen/python-fsa/workflows/CI/badge.svg)](https://github.com/bangyen/python-fsa/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python library for working with finite state automata (FSA), supporting both deterministic (DFA) and non-deterministic (NFA) automata with advanced operations including minimization, state combination, visualization, and more.

## Features

- **Complete FSA Support**: Both DFA and NFA implementations
- **Advanced Operations**: Minimization, state combination, unreachable state removal
- **Visualization**: Graphviz integration for FSA diagrams
- **Type Safety**: Full type hints and comprehensive error handling
- **Performance**: Optimized algorithms with efficient data structures
- **Extensible**: Clean API design for custom FSA implementations

## Installation

### From Source

```bash
git clone https://github.com/bangyen/python-fsa.git
cd python-fsa

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/bangyen/python-fsa.git
cd python-fsa

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
pre-commit install
```

### Alternative Installation Options

```bash
# Activate virtual environment first
source venv/bin/activate

# Install with specific dependency groups
pip install -e ".[test]"      # Testing dependencies only
pip install -e ".[lint]"      # Linting and formatting tools
pip install -e ".[docs]"      # Documentation tools
pip install -e ".[all]"       # All optional dependencies
```

## Quick Start

### Basic Usage

```python
from python_fsa import StateMachine

# Create a divisibility checker (binary numbers divisible by 3)
fsa = StateMachine.create_divisibility_checker(2, 3)

# Process input
result = fsa(1, 1)  # Binary 11 (decimal 3)
print(f"Accepted: {result.accept}")  # True

# Test different inputs
test_cases = [
    ([1, 1], "Binary 11 (decimal 3)"),
    ([1, 0, 1], "Binary 101 (decimal 5)"),
    ([1, 1, 0], "Binary 110 (decimal 6)")
]

for input_seq, description in test_cases:
    fsa_copy = StateMachine.create_divisibility_checker(2, 3)
    result = fsa_copy(*input_seq)
    print(f"{description}: {'ACCEPTED' if result.accept else 'REJECTED'}")
```

### Custom FSA Definition

```python
# Create a custom DFA that accepts strings ending in 'ab'
fsa = StateMachine({
    'S0': {'a': 'S1', 'b': 'S0', 'start': True, 'accept': False},
    'S1': {'a': 'S1', 'b': 'S2', 'start': False, 'accept': False},
    'S2': {'a': 'S1', 'b': 'S0', 'start': False, 'accept': True}
})

# Test strings
test_strings = ['ab', 'aab', 'baab', 'abab', 'ba']
for test_str in test_strings:
    fsa_copy = StateMachine({
        'S0': {'a': 'S1', 'b': 'S0', 'start': True, 'accept': False},
        'S1': {'a': 'S1', 'b': 'S2', 'start': False, 'accept': False},
        'S2': {'a': 'S1', 'b': 'S0', 'start': False, 'accept': True}
    })
    result = fsa_copy(*list(test_str))
    print(f"'{test_str}': {'ACCEPTED' if result.accept else 'REJECTED'}")
```

### NFA Support

```python
# Create an NFA that accepts strings containing 'ab' or 'ba'
nfa = StateMachine({
    'S0': {'a': ['S0', 'S1'], 'b': ['S0', 'S2'], 'start': True, 'accept': False},
    'S1': {'b': 'S3', 'start': False, 'accept': False},
    'S2': {'a': 'S3', 'start': False, 'accept': False},
    'S3': {'a': 'S3', 'b': 'S3', 'start': False, 'accept': True}
})
```

## Advanced Features

### DFA Minimization

```python
# Create a DFA that can be minimized
fsa = StateMachine({
    'S0': {0: 'S1', 1: 'S2', 'start': True, 'accept': False},
    'S1': {0: 'S0', 1: 'S3', 'start': False, 'accept': False},
    'S2': {0: 'S4', 1: 'S5', 'start': False, 'accept': True},
    'S3': {0: 'S4', 1: 'S5', 'start': False, 'accept': True},
    'S4': {0: 'S4', 1: 'S5', 'start': False, 'accept': True},
    'S5': {0: 'S5', 1: 'S5', 'start': False, 'accept': False}
})

print(f"Before minimization: {len(fsa.fsa)} states")
minimized = fsa.minimize()
print(f"After minimization: {len(minimized.fsa)} states")
```

### State Combination (NFA to DFA)

```python
# Combine NFA states for DFA conversion
nfa = StateMachine({
    'S0': {0: 'S0', 1: ['S0', 'S1'], 'start': True, 'accept': False},
    'S1': {0: 'S1', 1: 'S1', 'start': False, 'accept': True}
})

combined_state = nfa.combine_states('S0', 'S1')
print(combined_state)
```

### Visualization

```python
# Create a graph visualization
fsa = StateMachine.create_divisibility_checker(10, 2)
graph = fsa.create_graph()

# Render to file (requires Graphviz)
graph.render('divisibility_by_2', format='png')
```

## API Reference

### StateMachine Class

#### Constructor
- `StateMachine(fsa_definition)` - Create FSA from dictionary definition

#### Factory Methods
- `StateMachine.create_divisibility_checker(base, divisor)` - Create divisibility checker

#### Core Methods
- `__call__(*inputs)` - Process input symbols through the FSA
- `minimize()` - Minimize the DFA using table-filling algorithm
- `remove_unreachable_states()` - Remove states not reachable from start
- `combine_states(*state_names)` - Combine NFA states into single state
- `create_graph(**options)` - Create Graphviz visualization

#### Utility Methods
- `minimize_arrows(add_spaces=False)` - Optimize transition labels
- `__str__()` - Human-readable string representation

### FSA Definition Format

```python
fsa_definition = {
    'StateName': {
        'input_symbol': 'target_state',  # or ['state1', 'state2'] for NFA
        'start': True/False,
        'accept': True/False
    }
}
```

### Error Handling

The library provides comprehensive error handling with custom exceptions:

- `FSAError` - Base exception for all FSA errors
- `InvalidFSADefinitionError` - Invalid FSA definition
- `InvalidStateError` - Invalid state reference
- `InvalidTransitionError` - Invalid transition attempt
- `MinimizationError` - Minimization algorithm failure

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_automaton.py -v
```

### Code Quality

The project includes a simplified Makefile for common development tasks:

```bash
# Activate virtual environment first
source venv/bin/activate

# Run all quality checks (lint, type-check, test)
make check

# Format code
make format

# Run linting checks
make lint

# Run type checking
make type-check

# Run tests with coverage
make test

# Clean build artifacts
make clean

# Build package
make build

# Show all available commands
make help
```

Or run commands directly:

```bash
# Format code
black src tests
ruff check --fix src tests

# Lint code
ruff check src tests
black --check src tests

# Type checking
mypy src
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Examples

See the `examples/` directory for comprehensive usage examples:

- `basic_usage.py` - Core functionality demonstration
- `advanced_features.py` - Advanced features and error handling

## Performance

The library is optimized for performance with:

- Efficient state representation
- Optimized minimization algorithms
- Memory-conscious data structures
- Lazy evaluation where appropriate

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and code quality checks succeed
6. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classical automata theory and formal language processing
- Uses Graphviz for visualization
