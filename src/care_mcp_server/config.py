"""
Configuration management for Care MCP Server
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CareConfig:
    """Configuration for Care API integration."""

    # API URLs
    base_url: str = "https://careapi.ohc.network"
    schema_url: str = "https://careapi.ohc.network/api/schema/"
    swagger_url: str = "https://careapi.ohc.network/swagger/"

    # Authentication
    username: Optional[str] = None
    password: Optional[str] = None
    access_token: Optional[str] = None

    # Server settings
    server_name: str = "Care Healthcare Platform"
    server_version: str = "0.1.0"

    # Paths
    whitelist_file: Optional[Path] = None
    enhancements_file: Optional[Path] = None

    # HTTP settings
    timeout: int = 60
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> "CareConfig":
        """Create configuration from environment variables."""

        return cls(
            username=os.getenv("CARE_USERNAME"),
            password=os.getenv("CARE_PASSWORD"),
            access_token=os.getenv("CARE_ACCESS_TOKEN"),
            base_url=os.getenv("CARE_BASE_URL", "https://careapi.ohc.network"),
        )

    def validate_auth(self) -> bool:
        """Check if authentication credentials are available."""

        return bool(self.access_token or (self.username and self.password))


def load_config(config_path: Optional[Path] = None) -> CareConfig:
    """Load configuration from file or environment."""

    if config_path and config_path.exists():
        with open(config_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return CareConfig(**data)

    return CareConfig.from_env()
