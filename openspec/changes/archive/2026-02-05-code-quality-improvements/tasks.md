## 1. Implement Session Loading

- [x] 1.1 Research instaloader's session loading API and understand the expected format
- [x] 1.2 Update `_load_session()` method in `instaloader_client.py` to use `loader.context.load_session_from_file()` or equivalent
- [x] 1.3 Handle cases where session file doesn't exist or is invalid gracefully
- [x] 1.4 Update `_session_loaded` flag appropriately based on successful session loading

## 2. Add Update Checker Tests

- [x] 2.1 Create `tests/test_update_checker.py` file
- [x] 2.2 Add test for `get_installed_version()` function
- [x] 2.3 Add tests for `get_latest_version()` with mocked HTTP responses (success and failure cases)
- [x] 2.4 Add tests for `is_cache_valid()` (fresh cache, expired cache, no cache)
- [x] 2.5 Add tests for `check_for_updates()` including caching behavior and response structure
- [x] 2.6 Verify all tests pass

## 3. Enhance Error Messages

- [x] 3.1 Define error code constants/enum for different error types
- [x] 3.2 Update `fetch_instagram_post()` error handlers to include error codes
- [x] 3.3 Update `fetch_instagram_reel()` error handlers to include error codes
- [x] 3.4 Enhance error messages with more specific context where applicable
- [x] 3.5 Add retry hints for network errors if appropriate

## 4. Verify

- [x] 4.1 Run existing tests to ensure no regressions
- [x] 4.2 Run new update_checker tests
- [x] 4.3 Verify error responses include error codes in all cases
- [x] 4.4 Test session loading with valid and invalid session files
