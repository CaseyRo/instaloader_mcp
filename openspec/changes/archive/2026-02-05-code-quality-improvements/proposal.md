## Why

Improve code quality and maintainability by addressing three gaps: implementing proper session loading (currently a TODO), adding test coverage for the update checker module, and enhancing error messages with more actionable context.

## What Changes

- Implement proper instaloader session loading using the library's API instead of placeholder logic
- Add comprehensive tests for `update_checker.py` functions
- Enhance error messages in `server.py` with error codes, more specific context, and retry hints

## Capabilities

### New Capabilities
- `session-loading`: Proper session loading using instaloader's `load_session_from_file()` API
- `update-checker-tests`: Test coverage for update checking functionality
- `enhanced-error-messages`: More informative error responses with error codes and context

### Modified Capabilities
- `error-handling`: Enhanced error messages in `fetch_instagram_post` and `fetch_instagram_reel` tools

## Impact

- `src/instaloader_client.py`: Implement proper session loading in `_load_session()` method
- `src/server.py`: Enhance error responses with error codes and more context
- `tests/test_update_checker.py`: New test file with comprehensive coverage for update checker functions
