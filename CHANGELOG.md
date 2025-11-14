# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-14

### Added

- Initial release of Care MCP Server
- Token-based authentication with automatic refresh
- OpenAPI schema parser with $ref resolution
- Dynamic MCP tool generation from OpenAPI schema
- Whitelist manager for operation control (blocks destructive operations)
- AI-friendly metadata enhancements for key operations
- Pydantic-based configuration management
- FastMCP integration for tool registration
- Comprehensive test suite (34 tests with 100% pass rate)
- Support for environment variable configuration
- Claude Desktop integration support
- Detailed README with installation and usage instructions
- Example scripts demonstrating usage
- YAML import/export for whitelist configuration

### Core Modules

- `config.py` - Configuration management with Pydantic
- `auth.py` - Authentication handler with token refresh
- `schema_parser.py` - OpenAPI schema parser
- `whitelist.py` - Operation whitelist manager
- `enhancements.py` - AI-friendly metadata provider
- `tool_generator.py` - MCP tool generator
- `__main__.py` - Entry point with initialization flow

### Default Whitelisted Operations

- Facility: create, list, retrieve, update
- Organization: create, list, retrieve
- Location: create, list, retrieve
- Bed: create, list, retrieve, update
- Users: list, retrieve, getcurrentuser
- Geography: state_list, district_list, localBody_list, ward_list

### Documentation

- Comprehensive README.md
- USAGE.md with detailed usage guide
- CONTRIBUTING.md with contribution guidelines
- Code examples and demo scripts
- API documentation in docstrings

### Testing

- Unit tests for all core modules
- Configuration validation tests
- Schema parsing tests
- Whitelist management tests
- Enhancement metadata tests
- Code formatted with Black
- Linted with Ruff (zero issues)

## [Unreleased]

### Planned

- Integration tests with live Care API
- Additional operation enhancements
- CLI commands for whitelist management
- Enhanced error messages and logging
- Performance optimizations
- Docker support
- CI/CD pipeline
- More comprehensive documentation
