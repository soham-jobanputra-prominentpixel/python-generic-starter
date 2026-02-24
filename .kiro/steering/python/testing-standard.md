---
inclusion: fileMatch
fileMatchPattern: 'tests/**/*.py'
---

# LLM Unit Testing Standard

This document defines the **mandatory unittest standards** that any LLM (or contributor) must follow when generating tests for this project.

The goal is:

* Maximum source coverage
* Intelligent, non-overlapping test cases
* Deterministic, isolated tests
* Proper mocking & patching
* Clean, maintainable structure

---

# 1️ Core Principles

## 1.1 Tests Must Be Deterministic

* No real network calls
* No real filesystem mutation (unless explicitly testing it)
* No randomness without fixed seeds
* No reliance on system clock without patching

If time, randomness, environment variables, or external services are used:
→ **They must be mocked or patched.**

---

## 1.2 Each Test Must Have a Single Responsibility

Each test should verify **exactly one behavior**.

Bad:

```python
def test_create_user():
    # tests validation
    # tests DB insert
    # tests logging
    # tests response formatting
```

Good:

```python
def test_create_user_rejects_invalid_email():
    ...

def test_create_user_inserts_into_db():
    ...

def test_create_user_returns_serialized_response():
    ...
```

---

## 1.3 No Overlapping Test Cases

Tests must not redundantly verify the same behavior.

Before writing a test:

* Identify the execution path
* Ensure it exercises a **unique branch**
* Avoid duplicating assertion logic already covered

Each test should cover:

* A new branch
* A new failure path
* A new edge case
* Or a boundary condition

---

## 1.4 Maximize Branch Coverage

LLMs must:

* Identify all `if/else`
* All exception branches
* All early returns
* All validation branches
* All edge conditions

Every conditional path must be tested.

Example:

```python
if not user:
    raise ValueError("User not found")

if user.is_admin:
    return "admin"
else:
    return "user"
```

Required tests:

* user is None
* user is admin
* user is not admin

---

# 2️ Project Test Structure

All tests must:

* Live under `tests/`
* Mirror source folder structure
* Be named: `test_<module>.py`

Example:

```
src/services/auth.py
tests/services/test_auth.py
```

---

# 3️ unittest Standards

All tests must:

* Use `unittest.TestCase`
* Avoid print statements
* Avoid sleep
* Avoid shared mutable state

Basic structure:

```python
import unittest

class TestSomething(unittest.TestCase):

    def setUp(self):
        # Prepare clean environment
        pass

    def tearDown(self):
        # Clean up if needed
        pass

    def test_behavior_description(self):
        self.assertEqual(...)
```

---

# 4️ Mocking & Patching (MANDATORY WHEN REQUIRED)

Use:

```python
from unittest.mock import patch, MagicMock
```

Never manually monkey-patch.

---

## 4.1 Patching External Services

Example source:

```python
import requests

def fetch_data():
    response = requests.get("https://api.com/data")
    return response.json()
```

Test:

```python
@patch("src.services.module.requests.get")
def test_fetch_data_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"key": "value"}
    mock_get.return_value = mock_response

    result = fetch_data()

    self.assertEqual(result, {"key": "value"})
    mock_get.assert_called_once()
```

---

## 4.2 Patching Time

Source:

```python
from datetime import datetime

def get_current_year():
    return datetime.now().year
```

Test:

```python
@patch("src.module.datetime")
def test_get_current_year(mock_datetime):
    mock_datetime.now.return_value.year = 2025

    result = get_current_year()

    self.assertEqual(result, 2025)
```

---

## 4.3 Patching Environment Variables

```python
@patch.dict("os.environ", {"ENV": "production"})
def test_production_mode():
    ...
```

---

## 4.4 Patching Class Methods

```python
@patch.object(UserService, "save")
def test_user_saved(mock_save):
    mock_save.return_value = True
```

---

# 5️ Intelligent Test Case Design

LLMs must generate:

## 5.1 Boundary Tests

* Empty input
* Null input
* Maximum length
* Minimum length
* Zero values
* Negative values
* Large values

---

## 5.2 Failure Path Tests

Always test:

* Invalid inputs
* Exceptions
* Database failure
* API failure
* Timeout
* Permission errors

Every `raise` must have a test.

---

## 5.3 Property-Based Thinking (Without Overkill)

Tests should check:

* Invariants
* Idempotency
* Side effects

Example:

```python
def test_hash_is_deterministic():
    self.assertEqual(hash("x"), hash("x"))
```

---

## 5.4 Side-Effect Verification

If a function:

* Writes to DB
* Sends email
* Logs something
* Calls another function

Then assert it:

```python
mock_send_email.assert_called_once_with(...)
```

---

# 6️ Test Naming Rules

Use explicit naming:

```
test_<function>_<expected_behavior>_<condition>()
```

Examples:

* `test_login_returns_token_when_credentials_valid`
* `test_login_raises_error_when_password_incorrect`
* `test_calculate_discount_returns_zero_when_cart_empty`

Names must clearly explain:

* What is being tested
* Under what condition
* What outcome is expected

---

# 7️ Anti-Patterns (STRICTLY FORBIDDEN)

- Testing implementation details
- Testing private methods directly (unless absolutely required)
- Using real external APIs
- Using sleep()
- Relying on execution order
- Overlapping tests
- Giant tests covering multiple behaviors
- Copy-paste tests

---

# 8️ Coverage Expectations

Minimum target:

* 90%+ line coverage
* 100% branch coverage for critical modules

LLMs must:

* Analyze source file
* Identify all branches
* Generate required tests to cover them

If a branch cannot be tested:
→ Explicitly document why.

---

# 9️ Advanced Patterns (When Appropriate)

## 9.1 Parameterized Tests

If multiple similar cases exist:

```python
def test_is_even():
    cases = [
        (2, True),
        (3, False),
        (0, True),
        (-2, True),
    ]

    for value, expected in cases:
        with self.subTest(value=value):
            self.assertEqual(is_even(value), expected)
```

---

## 9.2 Testing Exceptions

```python
with self.assertRaises(ValueError):
    function_that_should_fail()
```

---

## 9.3 Verifying Log Calls

```python
@patch("src.module.logger")
def test_logs_error(mock_logger):
    ...
    mock_logger.error.assert_called_once()
```

---

# 10 LLM Generation Checklist (MANDATORY)

Before outputting test code, the LLM must verify:

* [ ] All branches covered
* [ ] All exceptions tested
* [ ] No overlapping cases
* [ ] No real external dependencies
* [ ] Mocks used correctly
* [ ] Each test has a single responsibility
* [ ] Assertions are meaningful (not trivial)
* [ ] Test names clearly explain behavior

---

# Definition of an Intelligent Test

An intelligent test:

* Validates behavior, not implementation
* Covers a unique execution path
* Tests both happy path and failure path
* Asserts side effects
* Ensures regressions are caught
* Improves confidence in correctness

---

# Final Rule

If an LLM generates tests that:

* Duplicate coverage
* Miss branches
* Skip failure paths
* Do not mock external dependencies

Then those tests are considered **invalid** and must be rewritten.

---

# Enforcement Policy

All generated tests must:

1. Pass locally
2. Increase coverage
3. Avoid redundancy
4. Improve long-term maintainability
