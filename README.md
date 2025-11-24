# Care MCP Server

A production-ready Model Context Protocol (MCP) server for the [Care Healthcare API](https://careapi.ohc.network). This server enables AI assistants like Claude to interact with healthcare facilities, organizations, locations, and bed management systems through a natural language interface.

## Features

- 🏥 **Healthcare Facility Management**: Create, list, retrieve, and update healthcare facilities
- 🏢 **Organization Management**: Manage health departments and organizations
- 📍 **Location Services**: Access geographic data (states, districts, local bodies, wards)
- 🛏️ **Bed Management**: Track and manage hospital bed capacity and availability
- 👤 **User Management**: Query user information and access control
- 🔐 **Secure Authentication**: Token-based authentication with automatic refresh
- 🔄 **Auto-generated Tools**: Dynamically generates MCP tools from OpenAPI schema
- 🎯 **Operation Whitelist**: Configurable control over allowed API operations
- 🤖 **AI-Friendly**: Enhanced metadata for better AI assistant interaction

## Installation

### Prerequisites

- Python 3.10 or higher
- Access to Care API (credentials required)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yash-learner/care_mcp_server.git
cd care_mcp_server

# Install dependencies
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

Create a `.env` file in the project root or set environment variables:

```bash
# Required: Care API Base URL
CARE_BASE_URL=https://careapi.ohc.network

# Required: Authentication (choose one method)
# Method 1: Username and Password
CARE_USERNAME=your_username
CARE_PASSWORD=your_password

# Method 2: Pre-existing Access Token
CARE_ACCESS_TOKEN=your_token

# Optional: Override schema URL
CARE_SCHEMA_URL=https://careapi.ohc.network/api/schema/
```

Copy `.env.example` as a starting point:

```bash
cp .env.example .env
# Edit .env with your credentials
```

## Usage

### Standalone Server

Run the server directly:

```bash
# Using the installed script
care-mcp-server

# Or using Python module
python -m care_mcp_server
```

### Integration with Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

#### macOS
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Windows
Location: `%APPDATA%\Claude\claude_desktop_config.json`

Configuration:

```json
{
  "mcpServers": {
    "care": {
      "command": "python",
      "args": ["-m", "care_mcp_server"],
      "env": {
        "CARE_BASE_URL": "https://careapi.ohc.network",
        "CARE_USERNAME": "your_username",
        "CARE_PASSWORD": "your_password"
      }
    }
  }
}
```

After adding the configuration:
1. Restart Claude Desktop
2. Look for the 🔌 icon to confirm the server is connected
3. Start using natural language commands!

### Example Queries

Once connected, you can ask Claude:

- "List all hospitals in Maharashtra"
- "Create a new healthcare facility named City General Hospital"
- "Show me available ICU beds in district X"
- "Get details of facility ID 123"
- "What organizations are registered in the system?"
- "List all states available in the system"

## Project Structure

```
care-mcp-server/
├── src/care_mcp_server/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Entry point
│   ├── config.py            # Configuration management
│   ├── auth.py              # Authentication handler
│   ├── schema_parser.py     # OpenAPI schema parser
│   ├── tool_generator.py    # MCP tool generator
│   ├── whitelist.py         # Operation whitelist manager
│   └── enhancements.py      # AI-friendly metadata
├── tests/                   # Test suite
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
├── .env.example            # Environment configuration template
└── .gitignore              # Git ignore rules
```

## Architecture

### Components

1. **Config** (`config.py`): Manages environment variables and configuration using Pydantic
2. **Auth Handler** (`auth.py`): Handles token-based authentication with automatic refresh
3. **Schema Parser** (`schema_parser.py`): Fetches and parses OpenAPI/Swagger schema
4. **Whitelist Manager** (`whitelist.py`): Controls which API operations are allowed
5. **Enhancement Manager** (`enhancements.py`): Provides AI-friendly metadata for operations
6. **Tool Generator** (`tool_generator.py`): Dynamically generates MCP tools from schema
7. **Main** (`__main__.py`): Orchestrates initialization and starts the MCP server

### Authentication Flow

1. Load credentials from environment variables
2. POST to `/api/v1/auth/login` with username/password
3. Extract `access_token` and `refresh_token`
4. Use Bearer token in Authorization header for API calls
5. Automatically refresh token when expired (1-hour default lifetime)

### Tool Generation Process

1. Fetch OpenAPI schema from Care API
2. Extract all API operations (paths + methods)
3. Filter operations through whitelist
4. Enhance whitelisted operations with AI-friendly metadata
5. Generate async Python functions for each operation
6. Register functions as MCP tools with FastMCP
7. Start stdio transport for MCP communication

## Default Whitelisted Operations

The server includes these operations by default (safe setup operations only):

**Facilities**: `facility_create`, `facility_list`, `facility_retrieve`, `facility_update`

**Organizations**: `organization_create`, `organization_list`, `organization_retrieve`

**Locations**: `location_create`, `location_list`, `location_retrieve`

**Beds**: `bed_create`, `bed_list`, `bed_retrieve`, `bed_update`

**Users**: `users_list`, `users_retrieve`, `users_getcurrentuser`

**Geography**: `state_list`, `district_list`, `localBody_list`, `ward_list`

**Blocked**: All `_destroy` and `_delete` operations are blocked for safety

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=care_mcp_server

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=care_mcp_server --cov-report=html
```

## Security Considerations

- ⚠️ Never commit `.env` files or credentials to version control
- 🔒 Access tokens are sensitive - store them securely
- 🚫 Destructive operations (`_destroy`, `_delete`) are blocked by default
- 🔐 All API calls use HTTPS and Bearer token authentication
- ⏱️ Tokens automatically refresh to maintain secure sessions

## Troubleshooting

### Authentication Failed

- Verify credentials in `.env` file
- Check network connectivity to Care API
- Ensure API endpoint URLs are correct
- Try using a fresh access token if username/password fails

### Schema Loading Failed

- Verify `CARE_SCHEMA_URL` or ensure base URL is correct
- Check internet connectivity
- Ensure the Care API schema endpoint is accessible

### No Tools Generated

- Check that operations in the API match the whitelist
- Review console output for specific errors
- Verify the OpenAPI schema was fetched successfully

### Claude Desktop Connection Issues

- Verify `claude_desktop_config.json` syntax is valid JSON
- Check file path locations for your OS
- Restart Claude Desktop after configuration changes
- Check Claude Desktop logs for error messages

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run tests and linting
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [https://github.com/yash-learner/care_mcp_server/issues](https://github.com/yash-learner/care_mcp_server/issues)
- Care API Documentation: [https://careapi.ohc.network](https://careapi.ohc.network)

## Acknowledgments

- Built with [FastMCP](https://github.com/modelcontextprotocol/fastmcp)
- Powered by [Care API](https://careapi.ohc.network)
- Inspired by the Model Context Protocol standard
