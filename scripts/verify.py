#!/usr/bin/env python
"""Package verification script."""

import sys
from pathlib import Path


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists."""
    exists = Path(filepath).exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {filepath}")
    return exists


def main():
    """Run verification checks."""
    print("=" * 60)
    print("Care MCP Server - Package Verification")
    print("=" * 60)

    all_checks = []

    # Check documentation
    print("\n📚 Documentation Files:")
    all_checks.append(check_file_exists("README.md", "README"))
    all_checks.append(check_file_exists("USAGE.md", "Usage Guide"))
    all_checks.append(check_file_exists("CONTRIBUTING.md", "Contributing Guide"))
    all_checks.append(check_file_exists("CHANGELOG.md", "Changelog"))
    all_checks.append(check_file_exists("LICENSE", "License"))

    # Check configuration
    print("\n⚙️  Configuration Files:")
    all_checks.append(check_file_exists("pyproject.toml", "Project Config"))
    all_checks.append(check_file_exists(".env.example", "Environment Template"))
    all_checks.append(check_file_exists(".gitignore", "Git Ignore"))

    # Check source files
    print("\n🐍 Source Files:")
    all_checks.append(check_file_exists("src/care_mcp_server/__init__.py", "Package Init"))
    all_checks.append(check_file_exists("src/care_mcp_server/__main__.py", "Entry Point"))
    all_checks.append(check_file_exists("src/care_mcp_server/config.py", "Config Module"))
    all_checks.append(check_file_exists("src/care_mcp_server/auth.py", "Auth Module"))
    all_checks.append(
        check_file_exists("src/care_mcp_server/schema_parser.py", "Schema Parser")
    )
    all_checks.append(
        check_file_exists("src/care_mcp_server/whitelist.py", "Whitelist Manager")
    )
    all_checks.append(
        check_file_exists("src/care_mcp_server/enhancements.py", "Enhancements")
    )
    all_checks.append(
        check_file_exists("src/care_mcp_server/tool_generator.py", "Tool Generator")
    )

    # Check tests
    print("\n🧪 Test Files:")
    all_checks.append(check_file_exists("tests/__init__.py", "Test Init"))
    all_checks.append(check_file_exists("tests/test_config.py", "Config Tests"))
    all_checks.append(check_file_exists("tests/test_whitelist.py", "Whitelist Tests"))
    all_checks.append(check_file_exists("tests/test_enhancements.py", "Enhancement Tests"))
    all_checks.append(
        check_file_exists("tests/test_schema_parser.py", "Schema Parser Tests")
    )

    # Check examples
    print("\n📝 Examples:")
    all_checks.append(check_file_exists("examples/demo.py", "Demo Script"))

    # Import check
    print("\n📦 Package Import:")
    try:
        import care_mcp_server

        print(f"  ✓ Package imported successfully")
        print(f"    Version: {care_mcp_server.__version__}")
        print(f"    Description: {care_mcp_server.__description__}")
        all_checks.append(True)
    except ImportError as e:
        print(f"  ✗ Failed to import package: {e}")
        all_checks.append(False)

    # Summary
    print("\n" + "=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    print(f"Verification Results: {passed}/{total} checks passed")

    if passed == total:
        print("✅ All checks passed! Package is ready.")
        print("=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please review the issues above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
