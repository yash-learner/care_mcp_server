"""Main entry point for Care MCP Server."""

import asyncio
from datetime import datetime
from mcp.server.fastmcp import FastMCP

from .config import load_config
from .auth import AuthHandler
from .schema_parser import SchemaParser
from .whitelist import WhitelistManager
from .enhancements import EnhancementManager
from .tool_generator import ToolGenerator


def print_banner():
    """Print startup banner."""
    print("=" * 60)
    print("   Care MCP Server - Healthcare API Integration")
    print("=" * 60)
    print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


async def initialize() -> FastMCP:
    """
    Initialize and configure the MCP server.

    Returns:
        Configured FastMCP instance
    """
    print_banner()

    # Load configuration
    print("\n[1/6] Loading configuration...")
    config = load_config()

    if not config.has_credentials():
        print("ERROR: No credentials configured!")
        print("Please set CARE_USERNAME/CARE_PASSWORD or CARE_ACCESS_TOKEN in environment")
        raise ValueError("Missing authentication credentials")

    print(f"   Base URL: {config.care_base_url}")
    print(f"   Schema URL: {config.schema_url}")

    # Initialize auth handler and authenticate
    print("\n[2/6] Authenticating with Care API...")
    auth_handler = AuthHandler(config)

    if await auth_handler.authenticate():
        print("   ✓ Authentication successful")
    else:
        print("   ✗ Authentication failed")
        raise ValueError("Authentication failed")

    # Fetch OpenAPI schema
    print("\n[3/6] Fetching OpenAPI schema...")
    schema_parser = SchemaParser(config.schema_url)

    if await schema_parser.fetch_schema():
        operations = schema_parser.get_operations()
        print("   ✓ Schema loaded successfully")
        print(f"   Found {len(operations)} API endpoints")
    else:
        print("   ✗ Failed to fetch schema")
        raise ValueError("Failed to fetch OpenAPI schema")

    # Initialize whitelist and enhancements
    print("\n[4/6] Initializing operation filters...")
    whitelist_manager = WhitelistManager()
    enhancement_manager = EnhancementManager()

    allowed_operations = whitelist_manager.get_allowed_operations()
    print(f"   Whitelisted operations: {len(allowed_operations)}")

    # Initialize FastMCP
    print("\n[5/6] Creating MCP server...")
    mcp = FastMCP(name=config.server_name, version=config.server_version)

    # Generate and register tools
    print("\n[6/6] Generating MCP tools...")
    tool_generator = ToolGenerator(
        config=config,
        auth_handler=auth_handler,
        schema_parser=schema_parser,
        whitelist_manager=whitelist_manager,
        enhancement_manager=enhancement_manager,
        mcp=mcp,
    )

    tools_count = await tool_generator.generate_tools()
    print(f"   ✓ Generated {tools_count} MCP tools")

    # Print summary
    print("\n" + "=" * 60)
    print("   Server Ready!")
    print("=" * 60)
    print("\nAvailable operations:")
    for op in allowed_operations[:10]:  # Show first 10
        print(f"   • {op}")
    if len(allowed_operations) > 10:
        print(f"   ... and {len(allowed_operations) - 10} more")
    print("\n" + "=" * 60)

    return mcp


def main():
    """Main entry point."""
    try:
        # Initialize and run the server
        mcp = asyncio.run(initialize())

        # Run the server with stdio transport
        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
    except Exception as e:
        print(f"\n\nERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
