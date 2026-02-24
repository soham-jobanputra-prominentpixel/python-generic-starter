---
inclusion: fileMatch
fileMatchPattern: '**/*.py'
---

## Python Docstring Standards

All modules, classes, and public functions/methods require docstrings. Use `"""triple double quotes"""` for consistency.

---

## One-Line Docstrings

Use for simple, obvious cases. Write as imperative commands, not descriptions.

**Good**
```python
def get_user(user_id: int) -> User:
    """Fetch user by ID from database."""
```

**Bad**
```python
def get_user(user_id: int) -> User:
    """get_user(user_id) -> User"""  # Don't repeat signature
    """This function returns the user."""  # Not imperative
```

Rules:
- Closing quotes on same line
- No blank lines before/after
- End with period
- Describe effect as command ("Return X", "Calculate Y")

---

## Multi-Line Docstrings

Structure: summary line + blank line + details.

**Function/Method**
```python
def authenticate(username: str, password: str, *, remember: bool = False) -> Token:
    """Authenticate user and return access token.

    Args:
        username: User's login identifier
        password: Plain text password (hashed internally)
        remember: Extend token expiration to 30 days

    Returns:
        Token: Access token with expiration metadata

    Raises:
        AuthenticationError: Invalid credentials
        RateLimitError: Too many failed attempts
    """
```

**Class**
```python
class UserRepository:
    """Manage user persistence and retrieval.

    Handles database operations for user entities with caching.
    Thread-safe for read operations.

    Attributes:
        cache_ttl: Cache expiration in seconds (default: 300)
    """
```

**Module**
```python
"""User authentication and authorization.

Exports:
    authenticate() -- Verify credentials and issue token
    authorize() -- Check user permissions
    AuthenticationError -- Raised on invalid credentials
"""
```

Rules:
- Summary line fits on one line
- Blank line after summary
- Document args, returns, exceptions, side effects
- Closing quotes on separate line
- Blank line after class docstrings

---

## Argument Documentation

List each argument on separate line. Use correct parameter names (case-sensitive for keyword args).

```python
def process(data: dict, *, validate: bool = True, timeout: float = 30.0) -> Result:
    """Process incoming data with validation.

    Args:
        data: Input dictionary with 'id' and 'payload' keys
        validate: Run schema validation before processing
        timeout: Maximum processing time in seconds
    """
```

---

## Inheritance Documentation

Use "override" when replacing parent behavior, "extend" when calling parent method.

```python
class AdminUser(User):
    """User with elevated privileges.

    Extends User with admin-specific permissions and audit logging.
    """

    def save(self) -> None:
        """Save user and log admin action.

        Extends parent save() to include audit trail.
        """
```
