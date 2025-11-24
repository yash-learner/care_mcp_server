# Care MCP Server Usage Guide

This guide provides detailed instructions for setting up and using the Care MCP Server.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Configuration](#configuration)
3. [Claude Desktop Integration](#claude-desktop-integration)
4. [Advanced Usage](#advanced-usage)
5. [Troubleshooting](#troubleshooting)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yash-learner/care_mcp_server.git
cd care_mcp_server

# Install the package
pip install -e .
```

### Basic Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Care API credentials:
   ```bash
   CARE_BASE_URL=https://careapi.ohc.network
   CARE_USERNAME=your_username
   CARE_PASSWORD=your_password
   ```

3. Run the server:
   ```bash
   care-mcp-server
   ```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CARE_BASE_URL` | No | `https://careapi.ohc.network` | Base URL for Care API |
| `CARE_USERNAME` | Yes* | - | Username for authentication |
| `CARE_PASSWORD` | Yes* | - | Password for authentication |
| `CARE_ACCESS_TOKEN` | Yes* | - | Alternative to username/password |
| `CARE_SCHEMA_URL` | No | `{base_url}/api/schema/` | OpenAPI schema URL |

*Either username/password OR access_token is required.

### Configuration Examples

#### Using Username/Password

```bash
export CARE_BASE_URL=https://careapi.ohc.network
export CARE_USERNAME=myusername
export CARE_PASSWORD=mypassword
```

#### Using Access Token

```bash
export CARE_BASE_URL=https://careapi.ohc.network
export CARE_ACCESS_TOKEN=your_bearer_token_here
```

## Claude Desktop Integration

### macOS Configuration

1. Locate the configuration file:
   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. Add the Care MCP Server configuration:
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

3. Restart Claude Desktop

### Windows Configuration

1. Locate the configuration file:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add the same configuration as macOS (see above)

3. Restart Claude Desktop

### Linux Configuration

1. Locate the configuration file:
   ```bash
   ~/.config/Claude/claude_desktop_config.json
   ```

2. Add the same configuration as macOS (see above)

3. Restart Claude Desktop

### Verifying Connection

After restarting Claude Desktop:
- Look for the 🔌 icon in the interface
- Click it to see connected MCP servers
- "care" should appear in the list
- You can now use natural language to interact with the Care API

## Advanced Usage

### Custom Whitelist

Create a custom whitelist YAML file:

```yaml
# custom_whitelist.yaml
whitelist:
  - facility_list
  - facility_retrieve
  - bed_list
  - users_getcurrentuser

blocked_patterns:
  - _destroy
  - _delete
```

Load it in your code:

```python
from care_mcp_server.whitelist import WhitelistManager

manager = WhitelistManager.import_from_yaml('custom_whitelist.yaml')
```

### Programmatic Usage

```python
import asyncio
from care_mcp_server.config import Config
from care_mcp_server.auth import AuthHandler
from care_mcp_server.schema_parser import SchemaParser

async def main():
    # Initialize configuration
    config = Config(
        care_username="user",
        care_password="pass"
    )
    
    # Authenticate
    auth = AuthHandler(config)
    await auth.authenticate()
    
    # Fetch schema
    parser = SchemaParser(config.schema_url)
    await parser.fetch_schema()
    
    # Get operations
    operations = parser.get_operations()
    print(f"Found {len(operations)} operations")

asyncio.run(main())
```

### Adding Custom Enhancements

Extend the enhancements in your code:

```python
from care_mcp_server.enhancements import EnhancementManager, ToolEnhancement

manager = EnhancementManager()

# Add custom enhancement
manager.ENHANCEMENTS["my_operation"] = ToolEnhancement(
    title="🎯 My Custom Operation",
    description="Detailed description here",
    tags=["custom", "operation"],
    examples=["Example query 1", "Example query 2"]
)
```

## Troubleshooting

### Authentication Errors

**Problem:** "Authentication failed" error

**Solutions:**
- Verify username and password are correct
- Check if the Care API is accessible
- Try using an access token instead
- Ensure network connectivity to careapi.ohc.network

### Schema Loading Errors

**Problem:** "Failed to fetch schema" error

**Solutions:**
- Verify CARE_SCHEMA_URL is correct
- Check internet connectivity
- Ensure the schema endpoint is accessible
- Try accessing the schema URL directly in a browser

### No Tools Generated

**Problem:** Server starts but no tools are available

**Solutions:**
- Check that operations in the API match the whitelist
- Review console output for specific errors
- Verify the OpenAPI schema was fetched successfully
- Check whitelist configuration

### Claude Desktop Connection Issues

**Problem:** Care server doesn't appear in Claude Desktop

**Solutions:**
- Verify `claude_desktop_config.json` syntax is valid JSON
- Check file path is correct for your OS
- Restart Claude Desktop completely
- Check Claude Desktop logs for error messages
- Ensure Python is in your PATH

### Permission Errors

**Problem:** Permission denied errors when running the server

**Solutions:**
- Ensure you have proper permissions to read `.env` file
- Check Python installation has necessary permissions
- On Linux/macOS, ensure the script is executable: `chmod +x`

## Example Queries

Once connected to Claude Desktop, you can ask:

### Facility Management
- "List all hospitals in Kerala"
- "Create a new healthcare facility named City General Hospital"
- "Show me details of facility ID 123"
- "Update the phone number for facility ID 456"

### Bed Management
- "Show me available ICU beds in district X"
- "Create 10 oxygen beds in this facility"
- "What's the current bed capacity at this hospital?"
- "Update bed availability status"

### User Management
- "Who am I logged in as?"
- "List all users in the system"
- "Show me details for user ID 789"

### Geographic Queries
- "List all states in the system"
- "Show me districts in Maharashtra"
- "What local bodies are in this district?"
- "List all wards"

### Organization Management
- "List all health department organizations"
- "Create a new organization"
- "Show details of organization ID 101"

## Best Practices

1. **Security**
   - Never commit `.env` files or credentials to version control
   - Use environment variables for sensitive data
   - Rotate access tokens regularly
   - Review whitelisted operations before deployment

2. **Performance**
   - Token refresh happens automatically
   - Schema is cached after first fetch
   - Use specific queries to reduce API calls

3. **Error Handling**
   - Check console output for detailed error messages
   - Review API response status codes
   - Use try-catch blocks for custom integrations

4. **Maintenance**
   - Keep the package updated
   - Review whitelist periodically
   - Update enhancements for new operations
   - Monitor API changes and schema updates

## Support

For issues and questions:
- GitHub Issues: [https://github.com/yash-learner/care_mcp_server/issues](https://github.com/yash-learner/care_mcp_server/issues)
- Care API Documentation: [https://careapi.ohc.network](https://careapi.ohc.network)
