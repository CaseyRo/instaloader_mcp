## ADDED Requirements

### Requirement: Enhanced Error Messages
Error responses from fetch_instagram_post and fetch_instagram_reel SHALL include error codes, more specific context, and actionable information.

#### Scenario: Invalid URL format error

- **WHEN** fetch_instagram_post or fetch_instagram_reel receives an invalid URL format
- **THEN** the error response includes an `error_code` field (e.g., "INVALID_URL_FORMAT")
- **AND** the error message is clear and specific
- **AND** the response includes the invalid URL for reference

#### Scenario: Authentication required error

- **WHEN** fetch_instagram_post or fetch_instagram_reel encounters a LoginRequiredException
- **THEN** the error response includes an `error_code` field (e.g., "AUTHENTICATION_REQUIRED")
- **AND** the error message explains that authentication is needed
- **AND** the response includes guidance on how to provide session cookies

#### Scenario: Post/reel not found error

- **WHEN** fetch_instagram_post or fetch_instagram_reel cannot find the post/reel
- **THEN** the error response includes an `error_code` field (e.g., "POST_NOT_FOUND" or "REEL_NOT_FOUND")
- **AND** the error message indicates the post/reel was not found
- **AND** the response includes the requested URL/shortcode

#### Scenario: Network error

- **WHEN** fetch_instagram_post or fetch_instagram_reel encounters a network/connection error
- **THEN** the error response includes an `error_code` field (e.g., "NETWORK_ERROR")
- **AND** the error message indicates a network issue occurred
- **AND** the response may include retry hints if appropriate

#### Scenario: Unexpected error

- **WHEN** fetch_instagram_post or fetch_instagram_reel encounters an unexpected exception
- **THEN** the error response includes an `error_code` field (e.g., "UNEXPECTED_ERROR")
- **AND** the error message includes the exception message for debugging
- **AND** the response includes the requested URL for context
