"""
Care MCP Server
Auto-generated MCP server from Care API OpenAPI schema
"""

__version__ = "0.1.0"
__author__ = "yash-learner"

from .config import CareConfig
from .schema_parser import SchemaParser
from .auth import AuthHandler

__all__ = [
    "CareConfig",
    "SchemaParser",
    "AuthHandler",
]
