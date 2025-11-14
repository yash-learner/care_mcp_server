"""Configuration management for Care MCP Server."""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Configuration for Care MCP Server loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Configuration
    care_base_url: str = Field(
        default="https://careapi.ohc.network",
        description="Base URL for Care API"
    )
    
    care_schema_url: Optional[str] = Field(
        default=None,
        description="Schema URL (defaults to base_url + /api/schema/)"
    )
    
    # Authentication
    care_username: Optional[str] = Field(
        default=None,
        description="Username for Care API authentication"
    )
    
    care_password: Optional[str] = Field(
        default=None,
        description="Password for Care API authentication"
    )
    
    care_access_token: Optional[str] = Field(
        default=None,
        description="Pre-existing access token (alternative to username/password)"
    )
    
    # Server Settings
    server_name: str = Field(
        default="care-mcp-server",
        description="MCP server name"
    )
    
    server_version: str = Field(
        default="0.1.0",
        description="MCP server version"
    )
    
    @property
    def schema_url(self) -> str:
        """Get the full schema URL."""
        if self.care_schema_url:
            return self.care_schema_url
        return f"{self.care_base_url.rstrip('/')}/api/schema/"
    
    @property
    def login_url(self) -> str:
        """Get the login URL."""
        return f"{self.care_base_url.rstrip('/')}/api/v1/auth/login"
    
    def has_credentials(self) -> bool:
        """Check if credentials are configured."""
        return bool(
            self.care_access_token or 
            (self.care_username and self.care_password)
        )


def load_config() -> Config:
    """Load configuration from environment variables."""
    return Config()
