#!/usr/bin/env python
"""Example script demonstrating Care MCP Server usage.

This script shows how to configure and run the Care MCP Server.
"""

import os
from care_mcp_server.config import Config
from care_mcp_server.whitelist import WhitelistManager
from care_mcp_server.enhancements import EnhancementManager


def main():
    """Demonstrate Care MCP Server configuration."""
    print("=" * 60)
    print("Care MCP Server - Configuration Example")
    print("=" * 60)

    # Example 1: Load configuration from environment
    print("\n1. Configuration:")
    config = Config()
    print(f"   Base URL: {config.care_base_url}")
    print(f"   Schema URL: {config.schema_url}")
    print(f"   Login URL: {config.login_url}")
    print(f"   Has credentials: {config.has_credentials()}")

    # Example 2: Whitelist management
    print("\n2. Whitelist Operations:")
    whitelist = WhitelistManager()
    allowed_ops = whitelist.get_allowed_operations()
    print(f"   Total allowed operations: {len(allowed_ops)}")
    print(f"   Sample operations:")
    for op in allowed_ops[:5]:
        print(f"     - {op}")

    # Example 3: Enhancements
    print("\n3. AI-Friendly Enhancements:")
    enhancements = EnhancementManager()
    sample_ops = ["facility_create", "bed_list", "users_getcurrentuser"]
    for op in sample_ops:
        if enhancements.has_enhancement(op):
            enhancement = enhancements.get_enhancement(op)
            print(f"   {enhancement.title}")
            print(f"     Tags: {', '.join(enhancement.tags)}")

    print("\n" + "=" * 60)
    print("To run the server, set environment variables and execute:")
    print("   export CARE_USERNAME=your_username")
    print("   export CARE_PASSWORD=your_password")
    print("   care-mcp-server")
    print("=" * 60)


if __name__ == "__main__":
    main()
