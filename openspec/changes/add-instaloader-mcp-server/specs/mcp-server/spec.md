## ADDED Requirements

### Requirement: HTTP Transport MCP Server
The system SHALL implement a Model Context Protocol (MCP) server that uses HTTP transport for communication with MCP clients.

#### Scenario: Server accepts HTTP POST requests
- **WHEN** an MCP client sends a JSON-RPC 2.0 request via HTTP POST
- **THEN** the server SHALL process the request and return a JSON-RPC 2.0 response

#### Scenario: Protocol initialization
- **WHEN** a client initiates an MCP session
- **THEN** the server SHALL negotiate protocol version and capabilities according to MCP specification

#### Scenario: Error handling
- **WHEN** an invalid or malformed request is received
- **THEN** the server SHALL return a proper JSON-RPC error response with appropriate error code and message

### Requirement: Tool Registration
The system SHALL register MCP tools that can be discovered and invoked by MCP clients.

#### Scenario: Tool discovery
- **WHEN** a client requests available tools
- **THEN** the server SHALL return a list of registered tools including their names, descriptions, and parameter schemas

#### Scenario: Tool invocation
- **WHEN** a client invokes a registered tool with valid parameters
- **THEN** the server SHALL execute the tool and return results in the JSON-RPC response

### Requirement: Server Configuration
The system SHALL support configuration via environment variables in a `.env` file.

#### Scenario: Port configuration via .env
- **WHEN** the server starts
- **THEN** it SHALL read the `MCP_PORT` environment variable from `.env` file
- **AND** if `MCP_PORT` is set, use that port
- **AND** if `MCP_PORT` is not set, default to port 3336
- **AND** the server SHALL listen on the configured port
