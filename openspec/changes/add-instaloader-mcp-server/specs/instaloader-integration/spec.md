## ADDED Requirements

### Requirement: URL Parsing and Shortcode Extraction
The system SHALL parse full Instagram URLs and extract the post/reel shortcode (ID) from them.

#### Scenario: Extract shortcode from full URL
- **WHEN** a client provides a full Instagram URL (e.g., "https://www.instagram.com/p/DRr-n4XER3x/")
- **THEN** the system SHALL extract the shortcode (e.g., "DRr-n4XER3x") from the URL
- **AND** use the shortcode to fetch the post/reel using `instaloader`

#### Scenario: Handle shortcode directly
- **WHEN** a client provides a shortcode directly (e.g., "DRr-n4XER3x")
- **THEN** the system SHALL use the shortcode as-is to fetch the post/reel

#### Scenario: Handle invalid URL format
- **WHEN** a client provides a URL that does not match Instagram URL patterns
- **THEN** the system SHALL return an error indicating the URL format is invalid

### Requirement: Fetch Instagram Post
The system SHALL provide a tool to fetch an Instagram post by URL or shortcode and return its text content as JSON.

#### Scenario: Fetch public post without authentication
- **WHEN** a client invokes the tool with a valid Instagram post URL or shortcode
- **AND** no session cookie is provided
- **AND** the post is public
- **THEN** the system SHALL parse the URL to extract the shortcode (if needed)
- **AND** fetch the post using `instaloader` with the shortcode
- **AND** extract the text content (caption)
- **AND** return a JSON response containing the post text and relevant metadata (post ID, author, timestamp, etc.)

#### Scenario: Fetch public reel without authentication
- **WHEN** a client invokes the tool with a valid Instagram reel URL or shortcode
- **AND** no session cookie is provided
- **AND** the reel is public
- **THEN** the system SHALL parse the URL to extract the shortcode (if needed)
- **AND** fetch the reel using `instaloader` with the shortcode
- **AND** extract the text content (caption)
- **AND** return a JSON response containing the reel text and relevant metadata

#### Scenario: Fetch private post with session cookie
- **WHEN** a client invokes the tool with a valid Instagram post URL or shortcode
- **AND** a valid session cookie is provided
- **AND** the post is private
- **THEN** the system SHALL parse the URL to extract the shortcode (if needed)
- **AND** use the session cookie to authenticate
- **AND** fetch the post using `instaloader` with the session and shortcode
- **AND** extract and return the text content as JSON

#### Scenario: Handle invalid URL or shortcode
- **WHEN** a client invokes the tool with an invalid URL or shortcode
- **THEN** the system SHALL return an error response indicating the URL is invalid or the post/reel could not be found

#### Scenario: Handle private content without authentication
- **WHEN** a client invokes the tool with a private post/reel URL
- **AND** no session cookie is provided or the cookie is invalid
- **THEN** the system SHALL return an error response indicating authentication is required

#### Scenario: Handle network errors
- **WHEN** a network error occurs while fetching content
- **THEN** the system SHALL return an appropriate error response with details about the failure

### Requirement: Session Cookie Support
The system SHALL support optional session cookies for accessing private Instagram content.

#### Scenario: Optional cookie parameter
- **WHEN** a client invokes a tool
- **THEN** the session cookie parameter SHALL be optional
- **AND** the tool SHALL work without cookies for public content

#### Scenario: Cookie file configuration
- **WHEN** a cookie file path is specified via `COOKIE_FILE` environment variable in `.env`
- **THEN** the system SHALL read session cookies from the specified file
- **AND** use them for authenticated requests when needed

#### Scenario: Cookie format validation
- **WHEN** a session cookie is provided (via parameter or file)
- **THEN** the system SHALL validate the cookie format
- **AND** use it to create an authenticated `instaloader` session

### Requirement: JSON Response Format
The system SHALL return post and reel content in a structured JSON format.

#### Scenario: Response structure
- **WHEN** content is successfully fetched
- **THEN** the response SHALL include:
  - Post/reel text (caption)
  - Post/reel ID or shortcode
  - Author username
  - Timestamp
  - Update check information (if available)
  - Any other relevant metadata
