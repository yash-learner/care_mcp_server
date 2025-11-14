# Care MCP Server

Auto-generated MCP server for Care Healthcare API, enabling AI assistants to interact with the Care platform.

## Features

- 🏥 **Healthcare Facility Management** - Create and manage hospitals, clinics
- 🏢 **Organization Setup** - Configure healthcare organizations
- 📍 **Location Management** - Setup locations within facilities
- 🛏️ **Bed Management** - Track and allocate beds
- 🔐 **Secure Authentication** - Token-based API access
- ✅ **Whitelist Control** - Safe, controlled API access
- 🤖 **AI-Friendly** - Enhanced descriptions for natural language interaction

## Installation

```bash
# Clone repository
git clone https://github.com/yash-learner/care-mcp-server.git
cd care-mcp-server

# Install dependencies
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your Care API credentials:

```bash
CARE_USERNAME=your_username
CARE_PASSWORD=your_password
```

## Usage

### Run the server

```bash
# Using script entry point
care-mcp-server

# Or directly
python -m care_mcp_server
```

### Use with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "care-healthcare": {
      "command": "care-mcp-server",
      "env": {
        "CARE_USERNAME": "your_username",
        "CARE_PASSWORD": "your_password"
      }
    }
  }
}
```

## Project Structure

```
care-mcp-server/
├── src/care_mcp_server/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Entry point
│   ├── config.py            # Configuration management
│   ├── auth.py              # Authentication handler
│   ├── schema_parser.py     # OpenAPI parser
│   ├── tool_generator.py    # MCP tool generator
│   ├── whitelist.py         # API whitelist
│   └── enhancements.py      # Tool metadata
├── tests/                   # Test suite
├── pyproject.toml          # Project metadata
└── README.md               # This file
```

## Development

```bash
# Run tests
pytest

# Format code
black src/

# Lint
ruff check src/

# Type check
mypy src/
```

## License

MIT

## Author

yash-learner
