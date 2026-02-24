---
inclusion: fileMatch
fileMatchPattern: '**/*.py'
---

# Python Type Hints Reference

Quick reference for PEP 484 type annotations. Use this when writing or reviewing typed Python code.

## Core Principles

- Annotate function signatures (parameters and return types) always
- Annotate variables only when type cannot be inferred or when declaring without initialization
- Use modern syntax (Python 3.9+ for collections, 3.10+ for union operator)
- Prefer specific types over `Any` unless truly dynamic

## Variables

```python
# Explicit annotation (use when mypy cannot infer)
age: int = 1
name: str = "Alice"

# Declaration without initialization
pending: bool  # Assigned later in conditional logic

# Empty containers need explicit types
items: list[str] = []
cache: dict[str, int] = {}
result: str | None = None
```

## Built-in Types

```python
# Primitives
x: int = 1
x: float = 1.0
x: bool = True
x: str = "text"
x: bytes = b"data"

# Collections (Python 3.9+)
x: list[int] = [1, 2, 3]
x: set[str] = {"a", "b"}
x: dict[str, float] = {"key": 1.0}

# Tuples
x: tuple[int, str, bool] = (1, "a", True)  # Fixed size
x: tuple[int, ...] = (1, 2, 3)  # Variable size

# Union types (Python 3.10+)
x: int | str = 42
x: str | None = None  # Replaces Optional[str]
```

## Functions

```python
from collections.abc import Iterator, Callable

# Basic function
def process(data: str, count: int = 10) -> bool:
    return len(data) > count

# No return value
def log(message: str) -> None:
    print(message)

# Multiple return types
def parse(value: str) -> int | float:
    return int(value) if value.isdigit() else float(value)

# Callable types
def apply(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)

# Generators
def count_up(n: int) -> Iterator[int]:
    for i in range(n):
        yield i

# Variadic arguments
def format_log(*args: str, **kwargs: int) -> str:
    # args is tuple[str, ...]
    # kwargs is dict[str, int]
    return " ".join(args)

# Positional-only and keyword-only
def configure(host: str, /, *, port: int, timeout: int = 30) -> None:
    pass

configure("localhost", port=8080)  # Correct
# configure(host="localhost", port=8080)  # Error: host is positional-only
```

## Classes

```python
from typing import ClassVar

class Repository:
    # Class variable
    default_timeout: ClassVar[int] = 30

    def __init__(self, name: str, size: int = 0) -> None:
        # Instance variables inferred from parameters
        self.name = name
        self.size = size

    def add(self, item: str) -> None:
        self.size += 1

    @classmethod
    def create_empty(cls) -> "Repository":  # Forward reference
        return cls("empty")

# Classes as types
def backup(repo: Repository) -> bool:
    return repo.size > 0

# Subclasses accepted where parent expected
class CachedRepository(Repository):
    cache: dict[str, str]  # Explicit instance variable declaration

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.cache = {}

cached = CachedRepository("main")
backup(cached)  # Valid: subclass accepted
```

## Duck Types (Protocols)

Use abstract types when you need behavior, not concrete types.

```python
from collections.abc import Iterable, Sequence, Mapping, MutableMapping

# Iterable: anything usable in for loops
def sum_values(items: Iterable[int]) -> int:
    return sum(items)

sum_values([1, 2, 3])  # list
sum_values({1, 2, 3})  # set
sum_values(range(5))   # range

# Sequence: supports len() and indexing
def first_item(items: Sequence[str]) -> str:
    return items[0]

# Mapping: read-only dict-like
def get_config(settings: Mapping[str, str]) -> str:
    # settings["key"] = "value"  # Error: cannot mutate
    return settings.get("key", "default")

# MutableMapping: mutable dict-like
def update_config(settings: MutableMapping[str, str]) -> None:
    settings["updated"] = "true"  # OK
```

Why: Accepting `Iterable` instead of `list` makes functions work with any iterable (generators, sets, ranges), improving reusability.

## Type Narrowing

```python
def process(value: str | None) -> str:
    if value is None:
        return "default"
    # mypy knows value is str here
    return value.upper()

def handle(data: int | str) -> str:
    if isinstance(data, int):
        return str(data)  # data is int
    return data.upper()  # data is str

# Assert for logic mypy cannot infer
def get_user(user_id: int) -> str:
    user: str | None = fetch_user(user_id)
    assert user is not None, "User must exist"
    return user.upper()  # mypy knows user is str
```

## Advanced Patterns

```python
from typing import Any, TYPE_CHECKING, cast

# Any: escape hatch for truly dynamic code
def handle_dynamic(data: Any) -> Any:
    return data.whatever()  # No type checking

# cast: override inferred type (no runtime effect)
values: list[int] = [1, 2, 3]
strings = cast(list[str], values)  # Lie to mypy, no runtime check

# TYPE_CHECKING: conditional imports for type checking only
if TYPE_CHECKING:
    from expensive_module import ComplexType

def process(data: "ComplexType") -> None:  # String annotation avoids runtime import
    pass

# reveal_type: debugging tool (remove before commit)
x = [1, 2, 3]
reveal_type(x)  # Error: Revealed type is "builtins.list[builtins.int]"

# type: ignore: suppress false positives (document why)
result = legacy_function()  # type: ignore  # Returns None only on error, not in this context
```

## Forward References

```python
# Method 1: String annotation
def create_node(parent: "Node") -> "Node":
    pass

class Node:
    def add_child(self) -> "Node":
        return Node()

## Decorators

```python
from collections.abc import Callable
from typing import TypeVar

F = TypeVar('F', bound=Callable[..., Any])

# Decorator without arguments
def log_calls(func: F) -> F:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper  # type: ignore  # Wrapper signature differs

# Decorator with arguments
def retry(max_attempts: int) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass
        return wrapper  # type: ignore
    return decorator
```

## Async Code

```python
import asyncio

async def fetch_data(url: str, timeout: int = 30) -> str:
    await asyncio.sleep(1)
    return f"Data from {url}"

# Coroutines typed like regular functions
async def process_urls(urls: list[str]) -> list[str]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

## Common Patterns

### Optional with Default

```python
def connect(host: str, port: int | None = None) -> bool:
    actual_port = port if port is not None else 8080
    return True
```

### Multiple Return Types

```python
def parse_response(data: str) -> dict[str, Any] | None:
    if not data:
        return None
    return {"parsed": data}
```

### Generic Containers

```python
from typing import TypeVar

T = TypeVar('T')

def first_or_none(items: list[T]) -> T | None:
    return items[0] if items else None

result: int | None = first_or_none([1, 2, 3])  # T inferred as int
```

## Anti-Patterns

```python
# Bad: Untyped function (no checking)
def process(data):
    return data.upper()

# Good: Typed function
def process(data: str) -> str:
    return data.upper()

# Bad: Overusing Any
def handle(data: Any) -> Any:
    return data.process()

# Good: Specific types
def handle(data: dict[str, str]) -> str:
    return data.get("key", "")

# Bad: Redundant annotations when obvious
name: str = "Alice"  # Type is obvious
count: int = len(items)  # Return type is known

# Good: Annotate when needed
items: list[str] = []  # Empty container needs type
result: int | None = None  # Ambiguous without annotation
```

## Type Checking Commands

```bash
# Check single file
mypy script.py

# Check entire project
mypy .
```
