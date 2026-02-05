## Context

The codebase currently has three areas needing improvement:
1. Session loading is a placeholder that only checks file existence
2. Update checker module has no test coverage
3. Error messages are generic and lack actionable context

## Goals / Non-Goals

**Goals:**
- Implement proper instaloader session loading using the library's native API
- Add comprehensive test coverage for update_checker module
- Enhance error messages with error codes and more context

**Non-Goals:**
- Changing the public API or breaking existing functionality
- Adding new features beyond the three improvements
- Refactoring unrelated code

## Decisions

### Decision 1: Session Loading Implementation

**Approach:** Use instaloader's `loader.context.load_session_from_file()` method. The cookie_file path should point to the instaloader session directory (typically created by `instaloader --login username`), and we'll attempt to load the session file for the username if possible.

**Rationale:** This uses instaloader's native API, which handles session file format correctly. We'll maintain backward compatibility by gracefully handling cases where the session file doesn't exist or is invalid.

**Tradeoffs:** We may need to extract username from the session directory path or handle multiple session files. For now, we'll attempt to load sessions from the directory if it's a valid instaloader session directory.

### Decision 2: Test Structure for Update Checker

**Approach:** Create a new `test_update_checker.py` file with unit tests using pytest and mocking for HTTP calls.

**Rationale:** Keeps tests organized and allows mocking external dependencies (PyPI API) for reliable, fast tests.

**Tradeoffs:** Tests will need to mock httpx.AsyncClient and datetime for cache testing. We'll use pytest fixtures and async test markers.

### Decision 3: Error Code Format

**Approach:** Use uppercase snake_case error codes (e.g., `INVALID_URL_FORMAT`, `AUTHENTICATION_REQUIRED`) and include them in all error responses.

**Rationale:** Error codes enable programmatic error handling while maintaining human-readable messages. Consistent format makes them easy to document and use.

**Tradeoffs:** Adds a new field to error responses, but maintains backward compatibility since existing error structure is preserved.
