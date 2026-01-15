## ADDED Requirements

### Requirement: Instaloader Version Check
The system SHALL check for available updates to the `instaloader` Python module and include this information in responses.

#### Scenario: Check for updates
- **WHEN** the system processes a request
- **THEN** it SHALL check the latest available version of `instaloader` on PyPI
- **AND** compare it with the currently installed version

#### Scenario: Include update information in response
- **WHEN** a successful response is returned
- **THEN** the JSON response SHALL include update check information:
  - Current installed version of `instaloader`
  - Latest available version (if different)
  - Whether an update is available (boolean)

#### Scenario: Handle PyPI API errors gracefully
- **WHEN** the PyPI API is unavailable or returns an error
- **THEN** the system SHALL continue processing the request
- **AND** include a note in the response that update checking failed
- **AND** not fail the entire request due to update check failure

#### Scenario: Cache update check results
- **WHEN** multiple requests are processed within a short time period
- **THEN** the system SHALL cache update check results to avoid excessive API calls
- **AND** refresh the cache once per day
