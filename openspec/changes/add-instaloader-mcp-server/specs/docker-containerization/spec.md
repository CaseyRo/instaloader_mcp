## ADDED Requirements

### Requirement: Docker Container
The system SHALL be containerized in a Docker container that can be built and run locally.

#### Scenario: Dockerfile exists
- **WHEN** the project is examined
- **THEN** a Dockerfile SHALL be present
- **AND** it SHALL define a container that includes all dependencies and the MCP server code

#### Scenario: Build on the spot
- **WHEN** a user builds the Docker image
- **THEN** the build process SHALL work without requiring an external registry
- **AND** the image SHALL be built from source using `docker build`

#### Scenario: Container runs MCP server
- **WHEN** the Docker container is started
- **THEN** it SHALL automatically start the MCP HTTP server
- **AND** the server SHALL be accessible on a configured HTTP port

#### Scenario: Dependencies installed
- **WHEN** the Docker container is built
- **THEN** it SHALL install Python 3.5 or newer
- **AND** install UV package manager
- **AND** install the `instaloader` module and all other required dependencies using UV
- **AND** include the MCP server code

#### Scenario: Easy rebuild on updates
- **WHEN** `instaloader` or other dependencies are updated
- **THEN** users SHALL be able to rebuild the container easily
- **AND** the build process SHALL fetch the latest versions as specified

### Requirement: Container Configuration
The Docker container SHALL be configured with appropriate settings for running an MCP server.

#### Scenario: Port configuration
- **WHEN** the container is started
- **THEN** the HTTP port SHALL default to 3336
- **AND** the port SHALL be configurable via `MCP_PORT` environment variable in `.env` file
- **AND** the port SHALL be exposed in the Dockerfile

#### Scenario: Health check (optional)
- **WHEN** implemented
- **THEN** the container MAY include a health check endpoint
- **AND** Docker SHALL be able to verify the server is running

### Requirement: Docker Compose Configuration
The system SHALL provide a docker-compose.yml file for easy setup and execution.

#### Scenario: Docker Compose file exists
- **WHEN** the project is examined
- **THEN** a docker-compose.yml file SHALL be present
- **AND** it SHALL configure the MCP server container with appropriate settings

#### Scenario: Easy startup with docker-compose
- **WHEN** a user runs `docker-compose up`
- **THEN** the MCP server container SHALL start automatically
- **AND** all necessary configuration (ports, environment variables, volumes) SHALL be set up
- **AND** the server SHALL be accessible and ready to use

#### Scenario: Environment variable support in docker-compose
- **WHEN** docker-compose.yml is used
- **THEN** it SHALL support environment variables from `.env` file
- **AND** allow easy configuration of port and cookie file path
