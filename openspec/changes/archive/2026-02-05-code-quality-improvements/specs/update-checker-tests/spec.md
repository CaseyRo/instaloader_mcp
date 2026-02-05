## ADDED Requirements

### Requirement: Update Checker Test Coverage
The update_checker module SHALL have comprehensive test coverage for all public functions.

#### Scenario: Test get_installed_version

- **WHEN** `get_installed_version()` is called
- **THEN** it returns a non-empty version string
- **AND** the version string matches instaloader's `__version__` attribute

#### Scenario: Test get_latest_version success

- **WHEN** `get_latest_version()` is called and PyPI API responds successfully
- **THEN** it returns the latest version string from PyPI
- **AND** the version string is non-empty

#### Scenario: Test get_latest_version failure

- **WHEN** `get_latest_version()` is called and PyPI API fails or times out
- **THEN** it returns None
- **AND** no exception is raised

#### Scenario: Test is_cache_valid with fresh cache

- **WHEN** `is_cache_valid()` is called after cache was set less than 1 day ago
- **THEN** it returns True

#### Scenario: Test is_cache_valid with expired cache

- **WHEN** `is_cache_valid()` is called after cache was set more than 1 day ago
- **THEN** it returns False

#### Scenario: Test is_cache_valid with no cache

- **WHEN** `is_cache_valid()` is called when no cache exists
- **THEN** it returns False

#### Scenario: Test check_for_updates with caching

- **WHEN** `check_for_updates()` is called multiple times within the cache duration
- **THEN** subsequent calls return cached results without making HTTP requests
- **AND** the cached result matches the first call's result

#### Scenario: Test check_for_updates updates cache after expiry

- **WHEN** `check_for_updates()` is called after cache expiry
- **THEN** it fetches fresh data from PyPI
- **AND** updates the cache with new data

#### Scenario: Test check_for_updates response structure

- **WHEN** `check_for_updates()` is called
- **THEN** it returns a dictionary with keys: `installed_version`, `latest_version`, `update_available`, `update_check_error`
- **AND** `installed_version` is always a string
- **AND** `latest_version` is either a string or None
- **AND** `update_available` is a boolean
- **AND** `update_check_error` is either None or a string
