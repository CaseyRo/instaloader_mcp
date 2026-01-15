## ADDED Requirements

### Requirement: Test Suite with Example URLs
The system SHALL provide a test suite that can run a series of tests using URLs from an example text file.

#### Scenario: Test file exists
- **WHEN** the project is examined
- **THEN** an example test file (e.g., `tests/example_urls.txt`) SHALL be present
- **AND** it SHALL contain at least the following URLs:
  - "https://www.instagram.com/p/DRr-n4XER3x/"
  - "https://www.instagram.com/p/DTDy4fMDCc4/"
  - "https://www.instagram.com/p/DQUVv9kANPh/"
  - "https://www.instagram.com/p/DSNKaEZjIR9/"
- **AND** it MAY contain additional test URLs (posts and reels)

#### Scenario: Test runner executes tests
- **WHEN** a user runs the test suite
- **THEN** the system SHALL read URLs from the example test file
- **AND** execute tests for each URL
- **AND** verify that the MCP server can successfully fetch and extract text from each URL

#### Scenario: Test results reporting
- **WHEN** tests are executed
- **THEN** the system SHALL report:
  - Number of tests run
  - Number of tests passed
  - Number of tests failed
  - Details for any failures (error messages, URLs that failed)

#### Scenario: Test file format
- **WHEN** the example test file is examined
- **THEN** it SHALL contain one URL per line
- **AND** empty lines SHALL be ignored
- **AND** lines starting with `#` MAY be treated as comments

### Requirement: Automated Test Execution
The system SHALL provide a way to run the test suite automatically.

#### Scenario: Test command available
- **WHEN** a developer wants to run tests
- **THEN** a command SHALL be available (e.g., `uv run pytest`, `python -m pytest`, or custom script)
- **AND** it SHALL execute all tests in the test suite

#### Scenario: Tests can run in Docker
- **WHEN** tests are run in the Docker container
- **THEN** the test suite SHALL execute successfully
- **AND** test results SHALL be accessible
