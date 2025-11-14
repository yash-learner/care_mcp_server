"""Tests for configuration module."""

from care_mcp_server.config import Config, load_config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    assert config.care_base_url == "https://careapi.ohc.network"
    assert config.server_name == "care-mcp-server"
    assert config.server_version == "0.1.0"


def test_config_schema_url_default():
    """Test schema URL defaults to base URL + /api/schema/."""
    config = Config(care_base_url="https://example.com")
    assert config.schema_url == "https://example.com/api/schema/"


def test_config_schema_url_override():
    """Test schema URL can be overridden."""
    config = Config(
        care_base_url="https://example.com", care_schema_url="https://custom.com/schema/"
    )
    assert config.schema_url == "https://custom.com/schema/"


def test_config_login_url():
    """Test login URL is constructed correctly."""
    config = Config(care_base_url="https://example.com")
    assert config.login_url == "https://example.com/api/v1/auth/login"


def test_config_has_credentials_with_token():
    """Test has_credentials returns True with access token."""
    config = Config(care_access_token="test_token")
    assert config.has_credentials() is True


def test_config_has_credentials_with_username_password():
    """Test has_credentials returns True with username and password."""
    config = Config(care_username="user", care_password="pass")
    assert config.has_credentials() is True


def test_config_has_credentials_without_credentials():
    """Test has_credentials returns False without credentials."""
    config = Config()
    assert config.has_credentials() is False


def test_config_has_credentials_with_only_username():
    """Test has_credentials returns False with only username."""
    config = Config(care_username="user")
    assert config.has_credentials() is False


def test_load_config():
    """Test load_config function."""
    config = load_config()
    assert isinstance(config, Config)
