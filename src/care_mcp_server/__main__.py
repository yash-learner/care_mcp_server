"""
Main entry point for Care MCP Server
"""

import asyncio
import logging
import sys
from datetime import datetime

from .auth import AuthHandler
from .config import load_config
from .enhancements import EnhancementManager
from .schema_parser import SchemaParser
from .tool_generator import ToolGenerator
from .whitelist import WhitelistManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point"""

    print("=" * 70)
    print("🏥 CARE MCP SERVER - Healthcare API Assistant")
    print("=" * 70)
    print(f"📅 Started: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("👤 User: yash-learner")
    print()

    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()

        # Initialize components
        logger.info("Initializing authentication...")
        auth_handler = AuthHandler(
            base_url=config.base_url,
            username=config.username,
            password=config.password,
        )

        # Authenticate if credentials provided
        if config.validate_auth():
            if not await auth_handler.authenticate():
                logger.warning("Authentication failed, proceeding without auth")
        else:
            logger.warning("No authentication credentials provided")

        # Load schema
        logger.info("Loading OpenAPI schema...")
        schema_parser = SchemaParser(config.schema_url)

        if not await schema_parser.load_schema():
            logger.error("Failed to load schema. Exiting.")
            sys.exit(1)

        # Initialize whitelist and enhancements
        logger.info("Loading whitelist and enhancements...")
        whitelist = WhitelistManager()
        enhancements = EnhancementManager()

        # Generate tools
        logger.info("Generating MCP tools...")
        generator = ToolGenerator(
            schema_parser=schema_parser,
            auth_handler=auth_handler,
            base_url=config.base_url,
            whitelist=whitelist,
            enhancements=enhancements,
            mcp_server_name=config.server_name,
        )

        tool_count = generator.generate_tools()

        print(f"\n🎉 Successfully generated {tool_count} tools!")
        print("\n📋 Available operations:")
        print("   • Create and manage healthcare facilities")
        print("   • Setup organizations and hierarchies")
        print("   • Configure locations within facilities")
        print("   • Manage beds and asset locations")
        print("   • Query geographic data (states, districts)")

        print("\n🚀 Starting MCP server...")
        print("=" * 70)

        # Run MCP server
        mcp_server = generator.get_mcp_server()
        mcp_server.run(transport="stdio")

    except KeyboardInterrupt:  # noqa: PIE786
        logger.info("\n👋 Shutting down gracefully...")
        sys.exit(0)

    except Exception as exc:  # noqa: BLE001
        logger.error("❌ Fatal error", exc_info=exc)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
